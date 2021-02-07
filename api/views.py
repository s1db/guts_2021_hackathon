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
        
        # check edit_charity in post request
        if not request.user.is_authenticated:
            return HttpResponse({"error":"Authentication Required"})
        
        charity_account = None
        try:
            charity_account = CharityAccount.objects.get(email = request.POST.get("email"))
        except Exception as e:
            return JsonResponse({"error":"User not found"})
        finally:
            if charity_account:
                user = authenticate(username=charity_account.user.username, password= request.POST.get("password"))
                if user is not None:
                    charity_account.charityname = request.POST.get("charityname")
                    charity_account.phone = request.post.get("phone")

                    # update location info
                    charity_account.address.postcode = request.POST.get("postcode")
                    longitude = request.POST.get("longitude")
                    latitude = request.POST.get("latitude")
                    charity_account.address.longitude = longitude
                    charity_account.address.latitude = latitude

                    charity_account.save()
                    return JsonResponse({"success":"User details updated"})
                else:
                    return JsonResponse({"error":"Invalid Credentials"})


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
       
        if request.POST.get("email"):
            email = request.POST.get("email")
            charity_email = request.POST.get("charity_email")
            order_date = request.POST.get("order_date")
            order_size = request.POST.get("order_size")

            if len(CharityAccount.objects.filter(email=charity_email)) == 0:
               return JsonResponse({"error":"Invalid request, no charity associated with this email"})
            
            food_req = FoodRequest.objects.create(
                user_email = email,
                charity = CharityAccount.objects.get(email=charity_email),
                order_date = timezone.make_aware(timezone.datetime.strptime(order_date, date_format)),
                order_size = order_size,
                has_confirmed = False,
                unique_auth = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(256)),
                expiry_date = timezone.now()+timedelta(hours=2)
            )
            html_message= render_to_string(
                "confirm_foodrequest.html", 
                {
                    "expiry_date": food_req.expiry_date.strftime('%d-%m-%Y %H:%M'),
                    "token":food_req.unique_auth,
                    }
                )
            send_mail(
                "Food Parcel Confirmation",
                "",
                EMAIL_HOST_USER,
                [str(food_req.user_email)],
                fail_silently=False,
                html_message=html_message
            )
            return JsonResponse({"success":"Request Created"})
        else:
            return JsonResponse({"error":"Invalid request, 'email' is missing from request"})

class ConfirmFoodRequest(View):
    
    def get(self, request):
        if not request.GET.get("auth"):
            return JsonResponse({"error":"Auth token missing"})
        auth_token = request.GET.get("auth")
        # retrieve associated record for auth token
        food_request = FoodRequest.objects.filter(unique_auth=auth_token, has_confirmed=False)
        if len(food_request)==0:
            return JsonResponse({"error":"Invalid Auth Token"})

        food_request = food_request[0]
        if food_request.expiry_date < timezone.now():
            return JsonResponse({"error":"Request has expired"})
        food_request.has_confirmed = True
        food_request.expiry_date = food_request.order_date
        food_request.save()

        html_message= render_to_string(
                "alert_charity_of_new_request.html", 
                {
                    "date": food_request.expiry_date.strftime('%d-%m-%Y'),
                    "time":food_request.expiry_date.strftime('%H:%M'),
                    "size":food_request.order_size,
                    "expiry_date":food_request.expiry_date.strftime('%d-%m-%Y %H:%M'),
                    }
                )
        send_mail(
            "Food Parcel Request",
            "",
            EMAIL_HOST_USER,
            [str(food_request.charity.email)],
            fail_silently=False,
            html_message=html_message
        )
        return JsonResponse({"success":"Request confirmed"})
        
class GetFoodRequestsCharity(View):

    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return JsonResponse({"error":"No email (charity) supplied"})
        charity = CharityAccount.objects.filter(email=email)
        if len(charity)==0:
            return JsonResponse({"error":"Invalid email address"})
        
        charity = charity[0]
        food_requests = FoodRequest.objects.filter(charity=charity, has_confirmed=True, expiry_date__gte=timezone.now()).order_by("order_date")
        return JsonResponse(serialize(food_requests))

class GetFoodRequestsUser(View):
    
    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return JsonResponse({"error":"No email (charity) supplied"})
        
        food_requests = FoodRequest.objects.filter(user_email=email, expiry_date__gte=timezone.now()).order_by("order_date")
        return JsonResponse(serialize(food_requests))

class CreateCharityAccountView(View):

    def get(self,request):
        
        return JsonResponse({"error":"Invalid Request"})
    
    def post(self, request):
        email = request.POST.get("email","")
        username = email[:email.find("@")]
        password = request.POST.get("password")
        charityname = request.POST.get("charityname","")
        phone = request.POST.get("phone","")
        postcode = request.POST.get("postcode")
        if email and password:
            (user,created) = User.objects.get_or_create(username=username)

            if len(CharityAccount.objects.filter(email=email))!=0:
                User.objects.get(username=user.username).delete()
                return JsonResponse({"error":"This account already exists"})

            if created:
                #create address object
                charityAddress = Address()
                charityAddress.postcode = postcode,
                
                charityAddress.latitude = float(equest.POST.get("latitude",10.00))
                charityAddress.longitude = float(request.POST.get("longitude",10.00))
            
                charityAddress.address_line_1 = request.POST.get("address","")
                charityAddress.address_line_2 = request.POST.get("address2","")
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
                return JsonResponse({"charity":serialize('json',[charity]), "charity_address":serialize('json',[charityAddress]), "charity_diet_options":serialize('json',[charity_entry])})
            else:
                return JsonResponse({"error":"Account already exists"})
        else:
            return JsonResponse({"error":"Email and password are required for account creation"})

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
        #check id present
        if not request.GET.get("email"):
            return JsonResponse({"error":"'id' missing from request"})
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
                return JsonResponse(charities)
            except Exception as e:
                print(e)
                return JsonResponse({"error":"Account does not exist"})

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
