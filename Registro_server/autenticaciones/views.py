from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import get_user_model  # Importa get_user_model

# Formulario para el registro de usuarios
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = get_user_model()  # Usa el modelo de usuario actual
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")

# Vista de autenticación
def auth_view(request):
    User = get_user_model()  # Obtiene el modelo de usuario actual
    if request.method == 'POST':
        if 'register' in request.POST:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])  # Establecer la contraseña encriptada
                user.save()
                auth_login(request, user)  # Iniciar sesión automáticamente después del registro
                return redirect('autenticaciones:home')  # Redirigir a la vista home
            else:
                return render(request, 'auth.html', {'form': form, 'error': 'Error en el registro', 'errors': form.errors})

        elif 'login' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user)  # Iniciar sesión
                return redirect('autenticaciones:home')  # Redirigir a la vista home
            else:
                return render(request, 'auth.html', {'error': 'Credenciales incorrectas'})

    else:
        form = UserRegistrationForm()  # Mostrar formulario vacío al acceder por GET

    return render(request, 'auth.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

def information_view(request):
    return render(request, 'information.html')

def logout(request):  # Renombrar la función de logout
    auth_logout(request)  # Cerrar sesión
    return redirect('autenticaciones:auth_view')  # Redirigir a la vista de autenticación


def about_view(request):
    return render(request, 'about.html') 