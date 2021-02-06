import json
from api.models import Address, CharityAccount, CharityDietaryOptions, DiertaryRequirements, User
from django.utils import timezone
from django.views import View
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from app.settings import EMAIL_HOST_USER


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
                return response
            except Exception as e:
                pass
            if created:
                # create user 
                user.set_password(password)
                charity = CharityAccount()
                charity.charityname = charityname
                charity.email = email
                charity.phone = phone
                charity.save(commit=False)
                
                #create address object
                charityAddress = Address()
                charityAddress.postcode = postcode,
                charityAddress.latitude = geoloc[0]
                charityAddress.longitude = geoloc[1]
                charityAddress.address_line_1 = request.POST.get("address","")
                charityAddress.save()
                charity.save(commit=True)

                # create charity food options
                charityDiet = DiertaryRequirements.objects.create()
                charity_entry = CharityDietaryOptions.objects.create(
                    charity = charity,
                    dietary_options = charityDiet
                )
                response.status_code = 200
                response.content = json.dumps({"charity":charity, "charity_address":charityAddress, "charity_diet_options":charity_entry})
            else:
                response.status_code=400
                response.content = json.dumps({"error":"An account already exists with this email"})
        else:
            response.status_code=400
            response.content = json.dumps({"error":"Email and password are required for account creation"})
        return response

class CharityListView(View):
    'returns list of all charities'
    def post(self,request):
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
            response.content = json.dumps(charities)
            response.status_code = 200
            response['message'] = "Ok"
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
