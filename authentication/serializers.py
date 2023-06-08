from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'nom', 'prenom', 'date_de_naissance', 'adr_email', 'password', 'localisation', 'numero_de_tel', 'description', 'photo_de_profile']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user















# from rest_framework import serializers
# from .models import User

# class AuthenticationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#         "id",
#         "username",
#         "nom",
#         "prenom",
#         "date_de_naissance",
#         "adr_email",
#         "password", 
#         "localisation",
#         "numero_de_tel",
#         "description",
#         "photo_de_profile",
#         )


    
  