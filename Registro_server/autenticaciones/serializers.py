# serializers.py
from rest_framework import serializers
from .models import CustomUser 
import re

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if CustomUser .objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está en uso.")
        return value

    def validate_username(self, value):
        if CustomUser .objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return value

    def create(self, validated_data):
        user = CustomUser (**validated_data)
        user.set_password(validated_data['password'])  # Hashear la contraseña
        user.save()
        return user