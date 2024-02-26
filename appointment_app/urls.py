
from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_view, name='appointment'), 
    path('confirmation/', views.confirmation_page, name='confirmation_page'),  
]
