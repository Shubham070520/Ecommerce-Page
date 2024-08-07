from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from Pet.models import Pet,Cart
from django.contrib.auth.models import User
from django.contrib import messages #to add message
from django.contrib.auth import authenticate,login,logout
 

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
    if request.method == 'GET': #if request method is  not mentioned it is by-default get
        return render(request,'register.html')
    else:
        #capture values entered by user
        #insert in db
        #redirect to login if registration is successful else registration page
        u = request.POST['username'] # to capture values  #name = 'username' defined in register.html......similarly for others
        e = request.POST['email']   # to capture values
        p = request.POST['password']  # to capture values
        cp = request.POST['confirm_pwd']  # to capture values
        # validation
        if u=='' or e=='' or p=='' or cp== '' :
            context = {'Error': "All fields are compulsory"}
            return render(request,'register.html',context)
        elif p != cp:
            context = {'Error': "Passwords don't match"}
            return render(request,'register.html',context)
        else:

        # o = User.objects.create (username= u,email=e,password=p) with this password is not encrypted
            u = User.objects.create (username= u,email=e)  #orm query
            u.set_password(p) #to set encrypted password
            u.save()
            messages.success(request,'Registered successfully,Please Login')
            return redirect('/login')
        
def userLogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        # if user is not None: #verified user
        #     login(request, user)
        #     return redirect('/')
        # else: #not verified
        #     context = {'Error': "Invalid Credentials"}
        #     return render(request, 'login.html', context)
        if user == None:
            context = {'Error': "Invalid Credentials"}
            return render(request, 'login.html', context)
        else:
            login(request, user)
            # messages.success(request,'Logged in successfully!')
            return redirect('/')
        # print(user)
        # return redirect('/')
        #what is session management and why to implement it ----asked in interview mock

def userLogout(request):
    logout(request)  #user object is in request
    messages.success(request,'Logged out successfully!')
    return redirect('/')       

def addtocart(request,pet_id):
    user_id = request.user.id
    context = {}
    if user_id == None:
        context['Error'] = "Please Login First"
        return render(request,'login.html',context)
    else:
        #cart will add if pet and user object is known
        users = User.objects.filter(id=user_id)
        pets = Pet.objects.filter(id=pet_id)
        
        cart = Cart.objects.create(pid = pets[0],uid = users [0])
        cart.save()
        messages.success(request,'Pet is added to cart!')
        return redirect('/')



        