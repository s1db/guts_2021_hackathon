from django.conf import settings
from django.contrib import admin
from django.db import router
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import jwt_views

admin.autodiscover()


urlpatterns = [
    path("me/", views.Profile.as_view(), name="me"),
    path("token/", jwt_views.Login.as_view(), name="token"),
    path(
        "token/refresh/", jwt_views.RefreshToken.as_view(),
        name="token-refresh"
    ),
    path("token/logout/", jwt_views.Logout.as_view(), name="logout"),
    path("ping/", views.Ping.as_view(), name="ping"),
    path("admin/", admin.site.urls),
    path("editcharityaccount/", views.EditCharityAccountView.as_view(), name="editcharityaccount"),
    path("createcharityaccount/", views.CreateCharityAccountView.as_view(), name="createcharityaccount"),
    path("charitylist/", views.CharityListView.as_view(), name="charitylist"),
    path("charity/", views.charityView.as_view(), name="viewcharity"),
    path("email/", views.TestEmail.as_view(), name="email"),
    path("charityaccount/", views.EditCharityAccountView.as_view(), name="charityaccount"),
    path('token-auth/', obtain_auth_token, name='api_token_auth'), 
    path('newfoodrequest/', views.NewFoodRequest.as_view(), name="newfoodrequest"),
    path('confirmfoodrequest/', views.ConfirmFoodRequest.as_view(), name="confirmfoodrequest"),
    path('getcharityfoodrequests/', views.GetFoodRequestsCharity.as_view(), name="getcharityfoodrequests"),
    path('getuserfoodrequests/', views.GetFoodRequestsUser.as_view(), name="getuserfoodrequests"),
    #user urls    
    path("createuseraccount/", views.CreateUserAccountView.as_view(), name="createuseraccount"),
    path("setuserdietarypreferences/", views.SetUserDietaryPreferences.as_view(), name="setuserdietarypreferences"),
    path("edituserprofile/", views.EditUserProfile.as_view(), name="edituserprofile"),
    path("singlesignon/", views.SingleSignOn.as_view(), name="singlesignon"),
    path("userlogin/", views.UserLogin.as_view(), name="userlogin"),

]

urlpatterns += [
    path("api-auth/", include('rest_framework.urls'))
]


if not settings.ON_SERVER:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

