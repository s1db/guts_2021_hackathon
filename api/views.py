from api.models import CharityAccount, User
from django.utils import timezone
from django.views import View
from django.core.serializers import serialize
from rest_framework import generics, response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse

from . import serializers

class Profile(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.User

    def get_object(self):
        return self.request.user

class EditCharityAccountView(View):
    'handle charity edit views'
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        response = HttpResponse(content_type="application/json")
        response['message'] = ""

        # check user making request is authenticated
        if not request.user.is_authenticated:
            response['message'] = "Authorisation Required"
            response.status_code = 401
        else:
            #check edit_charity in post request
            if request.POST.get("edit_charity"):
                user = None
                try:
                    user = CharityAccount.objects.get(email = request.POST.get("email"))
                except Exception as e:
                    print(e)
                    response.status_code = 404
                    response['message'] = "User not found"
                finally:
                    if user:
                        user.charityname = request.objects.get("charityname")
                        user.phone = request.objects.get("phone")
                        user.save()
                        response.status_code = 200
                        response['message'] = "User Updated"
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



class Ping(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        return response.Response({'now': timezone.now().isoformat()})
