from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
 

# # Create your views here.
# def home(request):
#     return render(request,'base.html')

def home(request):
    return render(request,'index2.html')