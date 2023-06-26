from django.urls import path, include
from authentication.views import SignUpView ,LoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
  
    path('signup/', SignUpView.as_view(), name='signup'),
    #path('login/', LoginView.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    #path('login/', obtain_auth_token, name='login'),
    path('auth/password/reset/', include('django_rest_passwordreset.urls', namespace='update_password')),
    

]
