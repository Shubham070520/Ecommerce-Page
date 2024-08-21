from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from Pet.models import Pet,Cart,Order
from django.contrib.auth.models import User
from django.contrib import messages #to add message
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q  #to write min and max values
import razorpay
import random
from django.core.mail import send_mail

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
        # if User.objects.get(username = u) is not None:
        #     context = {'Error': "Username already exists"}
        #     return render(request,'register.html',context)
        # else:
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
        user = User.objects.get(id=user_id)
        pet = Pet.objects.filter(id=pet_id).first()
        
        cart = Cart.objects.create(uid = user,pid = pet)
        cart.save()
        messages.success(request,'Pet is added to cart!')
        return redirect('/')
    
def showUserCart(request):
    user = request.user
    cart = Cart.objects.filter(uid=user.id)
    totalBill = 0
    for c in cart:
        totalBill = totalBill + c.pid.price*c.quantity
    context={}
    count = 0
    context['cart'] = cart
    context['totalBill'] = totalBill
    context['count'] = count 
    count = len(cart)
    return render(request,'showCart.html',context)

def removeCart(request,cartid):
    cart = Cart.objects.filter(id = cartid)
    cart.delete()
    messages.success(request,'Pet is removed from cart!')
    return redirect('/showCart')

def updateCart(request,opr,cartid):
    cart = Cart.objects.filter(id = cartid)
    if opr == 1:
        cart.update(quantity = cart[0].quantity+1)  #for update and delete we have to use filter......filter returns multiple query set
    else: #opr == 0
        cart.update(quantity = cart[0].quantity-1)
    return redirect('/showcart')     

def searchType(request,pet_type):
     petList = Pet.objects.filter(type= pet_type)
     context = {'pets':petList}
     return render (request,'index2.html',context)   

def searchRange(request):
     min = request.GET['min']
     max = request.GET['max']
     condition1 = Q(price__gte = min)
     condition2 = Q(price__lte = max)
     petList = Pet.objects.filter(condition1 & condition2)
     context = {'pets':petList}
     return render (request,'index2.html',context)

def sortPrice(request,dir):
    col=''
    if dir == 'asc':
        col='price'
        # petList = Pet.objects.order_by('price')
    else:
        col = '-price'
        # petList = Pet.objects.order_by('-price')
    petList = Pet.objects.all().order_by(col)
    context = {'pets':petList}
    return render (request,'index2.html',context)

def confirmOrder(request):
   user = request.user
   cart = Cart.objects.filter(uid = user.id )
   totalBill = 0
   for c in cart:
      totalBill += c.pid.price * c.quantity
   count = len(cart)
   context={}
   context['cart']=cart
   context['total']=totalBill
   context['count']=count  
   return render(request,'confirmorder.html',context)

def payment(request):
    user = request.user
    userCart = Cart.objects.filter(uid = user.id)
    totalBill = 0
    for c in userCart:
        totalBill += c.pid.price * c.quantity
    client = razorpay.Client(auth=("rzp_test_FQnn3Glqg1rhvn", "vqmZMvBVFrUgCNxBr59YBr7C"))
    data = { "amount": 500, "currency": "INR", "receipt": "" }
    payment = client.order.create(data=data)
    context = {'data' : payment}
    return render(request,'pay.html',context)

def placeOrder(request):
    user = request.user
    userCart = Cart.objects.filter(uid = user.id)
    order_id = random.randrange(10000,99999)
    #verify if order-id exist in db
    #while Order.objects.filter(orderid = order_id).exists():

    for c in userCart:
        order = Order.objects.create(orderid = order_id,uid = c.user,pid = c.pid,quantity = c.quantity)
        order.save()
        #clear cart
    userCart.delete()
    msg_body = "Order id is "+ str(order_id)
    customerEmail = user.email
    print(customerEmail)
    send_mail(
    "Order placed successfully",  #subject
    msg_body,
    "shubhamrane016@gmail.com",   #sender
    [customerEmail],
    fail_silently=False,
)
    messages.success(request,'Order is placed successfully!')
    return redirect("/")

