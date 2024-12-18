
from django.urls import path
from . import views

app_name = 'autenticaciones'
urlpatterns = [
    path('', views.auth_view, name='auth_view'),  
    path('home/', views.home, name='home'),
    path('information/', views.information_view, name='information'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about_view, name='about'),
]
