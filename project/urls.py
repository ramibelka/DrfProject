from django.contrib import admin
from django.urls import path ,include

urlpatterns = [

    path('admin/', admin.site.urls),
    #local apps
    path('api/', include('authentication.urls')),
    path('api/', include('articles.urls')),
    #addes rest apps 
    path("api-auth/", include("rest_framework.urls")),#login
    path("api/v1/dj-rest-auth/", include("dj_rest_auth.urls")), #for log in : api/v1/dj-rest-auth/login
    
]
#----using : dj_rest_auth.urls :
# Login: /api/v1/dj-rest-auth/login/
# Logout: /api/v1/dj-rest-auth/logout/
# Password change: /api/v1/dj-rest-auth/password/change/
# Password reset: /api/v1/dj-rest-auth/password/reset/
# Password reset confirm: /api/v1/dj-rest-auth/password/reset/confirm/
# User registration: /api/v1/dj-rest-auth/registration/
# User account verification:  