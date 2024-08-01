from django.urls import path
from Pet import views

urlpatterns=[
    path('',views.home),
    
]