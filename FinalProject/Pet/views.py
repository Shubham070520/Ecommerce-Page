from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from Pet.models import Pet
 

# # Create your views here.
# def home(request):
#     return render(request,'base.html')

def home(request):
    context={}
    data = Pet.objects.all()
    context['pets'] = data
    return render(request,'index2.html',context)

def showPetDetails(request,rid):
    context= {}
    data = Pet.objects.get(id=rid)
    context['pets'] = data
    return render(request,'details.html',context)
