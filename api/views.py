import json
from api.models import Address, CharityAccount, CharityDietaryOptions, DiertaryRequirements, User, UserDietaryPreferences
from django.utils import timezone
from django.views import View
from django.core.serializers import serialize
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from app.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from . import serializers

class Profile(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.User

    def get_object(self):
        return self.request.user

class EditCharityAccountView(View):
    'handle charity edit views'

    def post(self,request):
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
        charityname = request.POST.get("name","")
        phone = request.POST.get("phone","")

        postcode = request.POST.get("postcode")
        geoloc = request.POST.get("geolocation")
        if email and password:
            (user,created) = User.objects.get_or_create(username=username)
            try:
                CharityAccount.objects.get(email=email)
            except Exception as e:
                response.status_code=400
                response.content = json.dumps({"error":"An account already exists with this email"})
                return response
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
            response.status_code = 404
            response['message'] = "invalid request"
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


class CreateUserAccountView(View):

    def get(self, request):
        response = HttpResponse(content_type="application/json")
        response.status_code = 400
        response.content = json.dumps({"error": "Invalid Request"})
        return response

    def post(self, request):
        response = HttpResponse(content_type="application/json")
        email = request.POST.get("email", "")
        username = email[:email.find("@")]
        password = request.POST.get("password")
        print(email, password)

        if email and password:
            (user, created) = User.objects.get_or_create(username=username)
            print(created)

            if created: #email = unique
                # create user
                user.set_password(password)
                user.email = email
                user.save()

                response.status_code = 200
                response.content = json.dumps({"success": "user registerd"})
            else:
                response.status_code = 400
                response.content = json.dumps({"error": "An account already exists with this email"})
        else:
            response.status_code = 400
            response.content = json.dumps({"error": "Email and password are required for account creation"})
        return response


class SetUserDietaryPreferences(View):

    def get(self, request):
        response = HttpResponse(content_type="application/json")
        response.status_code = 400
        response.content = json.dumps({"error": "Invalid Request"})
        return response

    def post(self, request):
        response = HttpResponse(content_type="application/json")
        email = request.POST.get("email", "")
        preferences = request.POST.get("preferences", "{}")
        preferences = json.loads(preferences)

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user:
                try:
                    user_preference = UserDietaryPreferences.objects.get(user=user)
                except UserDietaryPreferences.DoesNotExist:
                    user_preference = UserDietaryPreferences()
                    user_preference.dietary_preferences = DiertaryRequirements()

                for p in preferences.keys():
                    if p == "has_halal" and preferences[p]==1:
                        user_preference.dietary_preferences.has_halal=True
                    elif p == "has_sanitary_products" and preferences[p]==1:
                        user_preference.dietary_preferences.has_sanitary_products = True
                    elif  p == "has_vegetarian" and preferences[p]==1:
                        user_preference.dietary_preferences.has_vegetarian = True
                    elif p == "has_vegan" and preferences[p] == 1:
                        user_preference.dietary_preferences.has_vegan = True
                    elif p == "has_kosher" and preferences[p] == 1:
                        user_preference.dietary_preferences.has_kosher = True
                    elif p == "has_gluten_free" and preferences[p] == 1:
                        user_preference.dietary_preferences.has_gluten_free = True
                    elif p == "has_lactose_free" and preferences[p] == 1:
                        user_preference.dietary_preferences.has_lactose_free = True
                    else:
                        pass
                user_preference.dietary_preferences.save()
                user_preference.user = user
                user_preference.save()

                response.status_code = 200
                response.content = json.dumps({"success": "preferences set successfully"})
            else:
                response.status_code = 400
                response.content = json.dumps({"error": "user doesn't exist"})
        else:
            response.status_code = 400
            response.content = json.dumps({"error": "No user specified"})
        return response

class EditUserProfile(View):

    def get(self, request):
        response = HttpResponse(content_type="application/json")
        response.status_code = 400
        response.content = json.dumps({"error": "Invalid Request"})
        return response

    def post(self, request):
        response = HttpResponse(content_type="application/json")
        email = request.POST.get("email", "")
        new_email = request.POST.get("new_email", "")
        new_pword = request.POST.get("new_pword", "")

        preferences = json.loads(request.POST.get("new_preferences", ""))

        if email:

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user:
                # update user
                if new_email:
                    user.email = new_email
                if new_pword:
                    user.set_password(new_pword)

                user_pref = UserDietaryPreferences.objects.get(user=user)
                diet = user_pref.dietary_preferences
                for p in preferences.keys():
                    if p == "has_halal":
                        if preferences[p]==1:
                            diet.has_halal=True
                        else:
                            diet.has_halal=False
                    elif p == "has_sanitary_products":
                        if preferences[p]==1:
                            diet.has_sanitary_products = True
                        else:
                            diet.has_sanitary_products = False
                    elif p == "has_vegetarian":
                        if preferences[p]==1:
                            diet.has_vegetarian = True
                        else:
                            diet.has_vegetarian = False
                    elif p == "has_vegan":
                        if preferences[p] == 1:
                            diet.has_vegan = True
                        else:
                            diet.has_vegan = False
                    elif p == "has_kosher":
                        if preferences[p] == 1:
                            diet.has_kosher = True
                        else:
                            diet.has_kosher = False
                    elif p == "has_gluten_free":
                        if preferences[p] == 1:
                            diet.has_gluten_free = True
                        else:
                            diet.has_gluten_free = False
                    elif p == "has_lactose_free":
                        if preferences[p] == 1:
                            diet.has_lactose_free = True
                        else:
                            diet.has_lactose_free = False
                    else:
                        pass
                diet.save()

                try:
                    user.save()
                    response.status_code = 200
                    response.content = json.dumps({"success": "profile updated" })
                except IntegrityError:
                    response.status_code=400
                    response.content=json.dumps({"error": "email already exist"})



            else:
                response.status_code = 400
                response.content = json.dumps({"error": "user doesn't exist"})
        else:
            response.status_code = 400
            response.content = json.dumps({"error": "No user specified"})
        return response




class SingleSignOn(View):

    def get(self, request):
        response = HttpResponse(content_type="application/json")
        response.status_code = 400
        response.content = json.dumps({"error": "Invalid Request"})
        return response

    def post(self, request):
        response = HttpResponse(content_type="application/json")
        email =request.POST.get("email", "")
        print(type(email), email)

        if email:
            import random, string
            (user, created) = User.objects.get_or_create(email=email)
            random_pword = "".join(random.sample(string.ascii_letters + string.digits + string.punctuation, 8))
            send_mail("Foodbank: temporary password",
                      f"Please login in with this password: \n {random_pword} \n.",
                      EMAIL_HOST_USER,
                      [email],
                      fail_silently=False)
            if created:
                user.username=email[:email.find("@")]
            user.set_password(random_pword)
            user.save()
            response.status_code = 200
            response.content=json.dumps({"success": "email sent"})

        else:
            response.status_code = 400
            response.content = json.dumps({"error": "No email entered"})
        return response

class UserLogin(View):

    def get(self, request):
        response = HttpResponse(content_type="application/json")
        response.status_code = 400
        response.content = json.dumps({"error": "Invalid Request"})
        return response

    def post(self, request):
        response = HttpResponse(content_type="application/json")
        email =request.POST.get("email", "")
        pword = request.POST.get("password", "")

        if email and pword:
            try:
                user = User.objects.get(email=email)
                if user.check_password(pword):
                    response.status_code = 200
                    response.content=json.dumps({'status': 'login success'})
                else:
                    response.status_code = 400
                    response.content=json.dumps({'error': 'wrong X email or password'})
            except User.DoesNotExist:
                response.status_code = 400
                response.content=json.dumps({'error': 'wrong email or password'})

        else:
            response.status_code = 400
            response.content = json.dumps({"error": "no username or password entered"})
        return response

class TestEmail(View):

    def get(self, request):
        send_mail(
            "Hello World",
            "This is a message",
            EMAIL_HOST_USER,
            ['uctyrandom@gmail.com'],
            fail_silently=False
        )
        return HttpResponse(json.dumps({"Email":"sent?"}), content_type="application/json")

class Ping(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        return response.Response({'now': timezone.now().isoformat()})
