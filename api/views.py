from datetime import timedelta
import json
import random
import string
from api.models import Address, CharityAccount, CharityDietaryOptions, DiertaryRequirements, FoodRequest, User
from django.utils import timezone
from django.views import View
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from rest_framework import generics, response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from app.settings import EMAIL_HOST_USER

date_format = '%Y-%m-%d %H:%M:%S'

from . import serializers

class Profile(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.User

    def get_object(self):
        return self.request.user

class EditCharityAccountView(View):
    'handle charity edit views'

    def post(self,request):
        permission_classes = (IsAuthenticated,)
        response = HttpResponse(content_type="application/json")
        
        # check edit_charity in post request
        if not request.user.is_authenticated:
            response.status_code = 401
            response.content =  json.dumps({"error":"Authentication Required"})
            return response
        
        charity_account = None
        try:
            charity_account = CharityAccount.objects.get(email = request.POST.get("email"))
        except Exception as e:
            print(e)
            response.status_code = 404
            response.content =json.dumps({"error":"User not found"})
        finally:
            if charity_account:
                user = authenticate(username=charity_account.user.username, password= request.POST.get("password"))
                if user is not None:
                    charity_account.charityname = request.POST.get("charityname")
                    charity_account.phone = request.post.get("phone")

                    # update location info
                    charity_account.address.postcode = request.POST.get("postcode")
                    geolocation = request.POST.get("geolocation")
                    charity_account.address.longitude = geolocation[0]
                    charity_account.address.latitude = geolocation[1]

                    charity_account.save()
                    response.status_code = 200
                    response.content = {"Success":"User details updated"}
                else:
                    response.status_code = 401
                    response.content =  {"error":"Invalid Credentials"}
                    
        return response

    def get(self, request):
        # return charity data

        response = HttpResponse(content_type="application/json")
        response['message'] = ""
        response.content = {}

        #check email present
        if not request.GET.get("email"):
            response.status_code = 400
            response['message'] = "'email' missing from request"
        else:
            email = request.GET.get("email")
            try: # check email exists
                response.content = serialize('json', CharityAccount.objects.filter(email=email))
                response.status_code = 200
                response['message'] = "Ok"
            except Exception as e:
                print(e)
                response.status_code = 404
                response['message'] = "Account does not exist"
        return response

class NewFoodRequest(View):

    def post(self, request):
        response = HttpResponse(content_type="application/json")
        if request.POST.get("email"):
            email = request.POST.get("email")
            charity_email = request.POST.get("charity_email")
            order_date = request.POST.get("order_date")
            order_size = request.POST.get("order_size")

            if len(CharityAccount.objects.filter(email=charity_email)) == 0:
                response.content = json.dumps({"error":"Invalid request, no charity associated with this email"})
                response.status_code = 400
                return response
            
            food_req = FoodRequest.objects.create(
                user_email = email,
                charity = CharityAccount.objects.get(email=charity_email),
                order_date = timezone.make_aware(timezone.datetime.strptime(order_date, date_format)),
                order_size = order_size,
                has_confirmed = False,
                unique_auth = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(256)),
                expiry_date = timezone.now()+timedelta(hours=2)
            )
            html_message= f"\
                Hello,<br/>\
                Please click the link below to confirm the following food parcel request:<br/><br/>\
                <a href='http://127.0.0.1:8000/confirm/?auth={food_req.unique_auth}'>Confirm Request</a><br/>\
                This request will expire at {food_req.expiry_date.strftime('%d-%m-%Y %H:%M')}<br/><br/>\
                Best Regards,<br/>\
                Foodbank Finders \
                "
            print(html_message)
            send_mail(
                "Food Parcel Confirmation",
                "",
                EMAIL_HOST_USER,
                [str(food_req.user_email)],
                fail_silently=False,
                html_message=html_message
            )
            response.content = json.dumps({"success":"Request Created"})
            response.status_code = 200
        else:
            response.content = json.dumps({"error":"Invalid request, 'email' is missing from request"})
            response.status_code = 400
        return response

class CreateCharityAccountView(View):

    def get(self,request):
        response = HttpResponse(content_type="application/json")
        response.status_code = 400
        response.content = json.dumps({"error":"Invalid Request"})
        return response
    
    def post(self, request):
        response = HttpResponse(content_type="application/json")
        email = request.POST.get("email","")
        username = email[:email.find("@")]
        password = request.POST.get("password")
        charityname = request.POST.get("charityname","")
        phone = request.POST.get("phone","")

        postcode = request.POST.get("postcode")
        geoloc = request.POST.get("geolocation")
        if email and password:
            (user,created) = User.objects.get_or_create(username=username)
            try:
                CharityAccount.objects.get(email=email)
                response.status_code=400
                response.content = json.dumps({"error":"An account already exists with this email"})
                if created:
                    User.objects.get(username=user.username).delete()
                return response
            except Exception as e:
                pass
            if created:
                #create address object
                charityAddress = Address()
                charityAddress.postcode = postcode,
                
                try:
                    charityAddress.latitude = geoloc[0]
                    charityAddress.longitude = geoloc[1]
                except Exception as e:
                    #error store dummy val
                    charityAddress.latitude = 12.12050
                    charityAddress.longitude = 12.12050
                charityAddress.address_line_1 = request.POST.get("address","")
                charityAddress.save()

                # create user 
                user.set_password(password)
                charity = CharityAccount()
                charity.user = user
                charity.charityname = charityname
                charity.email = email
                charity.phone = phone
                charity.address = charityAddress
                charity.save()

                # create charity food options
                charityDiet = DiertaryRequirements.objects.create()
                charity_entry = CharityDietaryOptions.objects.create(
                    charity = charity,
                    dietary_options = charityDiet
                )
                response.status_code = 200
                response.content = json.dumps({"charity":serialize('json',[charity]), "charity_address":serialize('json',[charityAddress]), "charity_diet_options":serialize('json',[charity_entry])})
            else:
                response.status_code=400
                response.content = json.dumps({"error":"An account already exists with this email"})
        else:
            response.status_code=400
            response.content = json.dumps({"error":"Email and password are required for account creation"})
        return response

class CharityListView(APIView):
    'returns list of all charities'
#    permission_classes = (IsAuthenticated,)
    def post(self,request):
        response = HttpResponse(content_type="application/json")
        response.status_code = 404
        response['message'] = "invalid request"
        return response

    def get(self,request):
        response = HttpResponse(content_type="application/json")
        response['message'] = ""
        response.content = {}
        #check email present
        try: # check email exists
            charities = {}
            for charity in CharityAccount.objects.all():
                charities[charity.email] = {
                    "charity":serialize('json',[charity]),
                    "address":serialize('json',[charity.address]),
                    "diet_options":serialize('json',[CharityDietaryOptions.objects.get(charity=charity).dietary_options])
                    }

            return JsonResponse(charities)
        except Exception as e:
            print(e)
            response.status_code = 200
            response.content = json.dumps({})
        return response

class charityView(View):
    def get(self, request):
        # return charity data
        response = HttpResponse(content_type="application/json")
        response['message'] = ""
        response.content = {}
        #check id present
        if not request.GET.get("email"):
            response.status_code = 400
            response['message'] = "'id' missing from request"
        else:
            email = request.GET.get("email")
            try: # check email exists
                charities = {}
                for charity in CharityAccount.objects.filter(email=email):
                    charities[charity.email] = {
                        "charity":serialize('json',[charity]),
                        "address":serialize('json',[charity.address]),
                        "diet_options":serialize('json',[CharityDietaryOptions.objects.get(charity=charity).dietary_options])
                    }
                response.content = json.dumps(charities)
                response.status_code = 200
                response['message'] = "Ok"
            except Exception as e:
                print(e)
                response.status_code = 404
                response['message'] = "Account does not exist"
        return response

class TestEmail(View):

    def get(self, request):
        try:
            send_mail(
                "Hello World",
                "This is a message",
                EMAIL_HOST_USER,
                ['nathanwelsh8@gmail.com'],
                fail_silently=False
            )
            resp = "sent"
        except Exception as e:
            resp = e
        return HttpResponse(json.dumps({"status":str(resp)}), content_type="application/json")

class Ping(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        return response.Response({'now': timezone.now().isoformat()})
