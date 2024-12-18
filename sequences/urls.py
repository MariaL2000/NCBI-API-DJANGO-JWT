from django.urls import path
from . import views

app_name='sequences'
urlpatterns = [
    path('sequence/', views.sequence_view, name='sequence' ),
    path('results/', views.results_view , name='results_view'),
    path('about/', views.about_view, name='about'), 
]