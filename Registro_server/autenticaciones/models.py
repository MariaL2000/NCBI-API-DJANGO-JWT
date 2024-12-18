from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
import re

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """Crea y devuelve un usuario con un correo electrónico y contraseña."""
        if not email:
            raise ValueError('El correo electrónico debe ser proporcionado')
        if not username:
            raise ValueError('El nombre de usuario debe ser proporcionado')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Almacena la contraseña de forma segura
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Crea y devuelve un superusuario con un correo electrónico y contraseña."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser (AbstractBaseUser , PermissionsMixin):
    """Modelo de usuario personalizado."""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()  # Asigna el CustomUser Manager

    USERNAME_FIELD = 'email'  # Usa el correo electrónico como el campo único para autenticación
    REQUIRED_FIELDS = ['username']  # Campos requeridos al crear un superusuario

    def clean(self):
        """Valida la unicidad del correo electrónico y el nombre de usuario."""
        super().clean()
        if CustomUser .objects.filter(email=self.email).exists():
            raise ValidationError("Este correo ya está en uso.")
        
        if CustomUser .objects.filter(username=self.username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")

    def validate_password(self, password):
        """Valida que la contraseña contenga al menos un carácter especial."""
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("La contraseña debe contener al menos un carácter especial.")