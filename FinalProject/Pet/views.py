from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from Pet.models import Pet
from django.contrib.auth.models import User
 

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

def registerUser(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        #capture values entered by user
        #insert in db
        #redirect to login if registration is successful else registration page
        u = request.POST['username'] #name = 'username' defined in register.html
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['confirm_pwd']
        if u=='' or e=='' or p=='' or cp== '' :
            context = {'Error': "All fields are compulsory"}
            return render(request,'register.html',context)
        elif p != cp:
            context = {'Error': "Passwords don't match"}
            return render(request,'register.html',context)
        else:

        # o = User.objects.create (username= u,email=e,password=p) with this password is not encrypted
            o = User.objects.create (username= u,email=e)  #orm query
            o.set_password(p) #to set encrypted password
            o.save()
            return redirect('/')

        