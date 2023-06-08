from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    list_display = ('username','email', 'first_name', 'last_name', 'date_de_naissance', 'localisation', 'numero_de_tel','description')
admin.site.register(User, CustomUserAdmin)

