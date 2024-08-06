from django.urls import path
from Pet import views

urlpatterns=[
    path('',views.home),
    path('details/<rid>',views.showPetDetails),
    path('register',views.registerUser),
    path('login',views.userLogin)
]