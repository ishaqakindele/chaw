from email.message import EmailMessage
from email.policy import default
from pickle import TRUE
import requests
import json
import uuid
from django.core.mail import EmailMessage
from django.conf import settings
from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#  password reset modules
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
#  password reset modules done

from techbro.models import * #import all models from models.py file here
from dashboard.models import * 
from cartt.models import * 
from techbro.forms import SignupForm
from dashboard.forms import ProfileUpdateForm

# Create your views here.
def index(request):
    #query the Database to pull objects out
    categories = Category.objects.all()[:6]
    specials = Dish.objects.filter(special=True)
    slide1 = Showcase.objects.get(pk=1)
    slide2 = Showcase.objects.get(pk=2)
    slide3 = Showcase.objects.get(pk=3)

    context = {
        'categories':categories,
        'specials':specials,
        'slide1':slide1,
        'slide2':slide2,
        'slide3':slide3,
    }
    
    return render(request, 'index.html', context)

def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)  
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users =User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset requested"
                    email_template_name = "password/password_reset_email.txt"
                    c={
                        "email":user.email,
                        "domain": '127.0.0.1:8000',     
                        'site_name': 'Refill',
                        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'ishaqakindele@gmail.com',[user.email], fail_silently= False)
                    except BadHeaderError:
                            return HttpResponse('invalid header found.')
                    return redirect ("password_reset/done/")   
    password_reset_form= PasswordResetForm()
    return render(request=request, template_name= "password/password_reset.html", context={"password_reset_form":password_reset_form}) 

def contact(request):
    return render(request, 'contact.html')
   

def all_food(request):
    all_meals = Dish.objects.all()
    categories = Category.objects.all()
    specials = Dish.objects.filter(special=True)

    context = {
        'all_meals':all_meals,
        'categories':categories,
        'specials':specials,
    }
    return render(request, 'all_food.html', context)

def categories(request):
    categories = Category.objects.all()
    specials = Dish.objects.filter(special=True)

    context = {
        'categories':categories,
        'specials':specials,
    }
    return render(request, 'categories.html', context)


def single_category(request, id):
    specials = Dish.objects.filter(special=True)
    categories = Category.objects.all()
    single_category = Dish.objects.filter(category_id = id)
    cat_title = Category.objects.get(pk=id)

    context = {
        'specials':specials,
        'categories':categories,
        'category': single_category,
        'cat_title': cat_title,
    }
    return render(request, 'category.html', context)

def detail(requset, id):
    specials = Dish.objects.filter(special=True)
    categories = Category.objects.all()
    detail = Dish.objects.get(pk=id)

    context = {
        'specials':specials,
        'categories':categories,
        'detail':detail,
    }
    return render(requset, 'detail.html', context) 
 
def signin(request):
    if request.method =='POST':
        myusername = request.POST['username']
        mypassword = request.POST['password']
        user = authenticate(request, username =myusername, password =mypassword)
        if user:
            login(request, user)
            messages.success(request, f'Dear {user.username}, your signin is successful,welcome!')
            return redirect('index')
        else:
            messages.warning(request, 'Username/Password is incorrect')  
            return redirect('signin')  
    return render(request,'signin.html',)


def signout(request):
    logout(request)
    messages.success(request, 'You have now signed out successfully!')
    return render(request,'signin.html',)  

def signup(request):
    # make a get request to pull out and display the SignupForm
    form = SignupForm()#instantiate the Signupform for a GET request
    if request.method == 'POST':
        phone = request.POST['phone']
        image = request.POST['image']
        form = SignupForm(request.POST)
        if form.is_valid():#test form for virus free, and declare valid
            userform = form.save()#save incomin data
            newuser = Profile(user = userform)
            newuser.first_name = userform.first_name
            newuser.last_name = userform.last_name
            newuser.email = userform.email
            newuser.phone = phone
            newuser.profile_pix = image
            newuser.save()
            messages.success(request, 'Signup successful')#send success message to your user
            login(request, userform)
            return redirect('index')#redirect the user to any page of your choice
        else:
            messages.error(request, form.errors)#send out error message(s)
            return redirect('signup')#if error occurs at signup attemt, keep user on signup page
    return render(request,'signup.html',) 


# dashboard configuration
@login_required(login_url='signin')
def dashboard(requset ):
    profile_data =Profile.objects.get(user__username=requset.user.username)
    context ={
        'profile_data':profile_data
    }
    return render(requset, 'dashboard.html', context)

@login_required(login_url='signin')
def profileupdate(request):
    profile_data = Profile.objects.get(user__username =request.user.username)
    form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Update successful')
            return redirect('dashboard')
        else:
            messages.error(request, form.errors) 
            return redirect('profileupdate')   
    context = {
        'form': form,
        'profile_data': profile_data,
    }        
    return render(request, 'profileupdate.html', context)
    

@login_required(login_url='signin')    
def passwordupdate(request):
    profile_data = Profile.objects.get(user__username =request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method =='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'password update successful')
            return redirect('profile')
        else:
            messages.error(request, form.errors)  
            return redirect('passwordupdate')  
    context = {
        'profile_data': profile_data,
        'form': form,
    }
    return render(request, 'profilepassword.html', context)      
# dashboard configuration done  

#shopcart 
@login_required(login_url='signin')    
def ordermeal(request):
    profile_data = Profile.objects.get(user__username =request.user.username)
    cart_no = profile_data.id
    if request.method == 'POST':
        quantityselected = int(request.POST['mealquantity'])
        meal = request.POST['mealid']
        mealselected = Dish.objects.get(pk=meal)
        cart = Shopcartt.objects.filter(user__username= request.user.username, paid=False)
        if cart:
            basket = Shopcartt.objects.filter(dish=mealselected.id, user__username= request.user.username, paid=False).first()
            if basket:
                basket.quantity += quantityselected
                basket.amount = basket.quantity *basket.c_price
                basket.save()
                messages.success(request, 'Your meal is being processed!')
                return redirect('all_food')
            else:
                neworder= Shopcartt()
                neworder.user = request.user
                neworder.dish = mealselected
                neworder.c_name = mealselected.name
                neworder.quantity = quantityselected
                neworder.c_price = mealselected.price
                neworder.amount = mealselected.price * quantityselected
                neworder.cart_code = cart_no
                neworder.paid = False
                neworder.save()
                messages.success(request, 'Your meal is being processed!')
                return redirect('all_food')
        else:
            newitem = Shopcartt()
            newitem.user = request.user
            newitem.dish = mealselected
            newitem.c_name = mealselected.name
            newitem.quantity = quantityselected
            newitem.c_price = mealselected.price
            newitem.amount =mealselected.price * quantityselected
            newitem.cart_code = cart_no
            newitem.paid = False
            newitem.save()
            messages.success(request, 'Your meal is being processed!')

    return redirect('all_food')

@login_required(login_url='signin')
def mycart(request):
    profile = Profile.objects.get(user__username = request.user.username)
    shopcart = Shopcartt.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for item in shopcart:
        subtotal += item.c_price * item.quantity
        vat = 0.075 * subtotal
        total = vat + subtotal
   
    context ={
        'profile': profile,
        'shopcart': shopcart,
        'subtotal': subtotal,
        'vat': vat,
        'total': total,
       
    }
    return render(request, 'cart.html', context)

@login_required(login_url='signin')
def deletemeal(request):
    if request.method == 'POST':
        meal = request.POST['dishid']
        deletedish = Shopcartt.objects.get(pk=meal)
        deletedish.delete()
        messages.success(request, 'meal item deleted successfully!')
    return redirect('mycart')


@login_required(login_url='signin')
def deleteallmeal(request):
    if request.method == 'POST':
        meal = request.POST['alldishid']
        deletealldish = Shopcartt.objects.filter()
        deletealldish.delete()
        messages.success(request, 'All meal item deleted successfully!')
    return redirect('mycart')  
#shopcart done
 
#decrease cart item quantity    
@login_required(login_url='signin')
def decrease(request):
    if request.method == 'POST':
        itemquantity= int(request.POST['decrease'])
        cartitem = request.POST['itemid']
        decreasecart = Shopcartt.objects.get(pk= cartitem)
        decreasecart.quantity -= itemquantity
        decreasecart.save ()
        messages.success(request, 'Quantity decrease.')
    return redirect('mycart')


#increase cart item quantity  
@login_required(login_url='signin')
def increase(request):

      if request.method == 'POST':
        itemquantity= int(request.POST['increase'])
        cartitem = request.POST['itemid']
        increasecart = Shopcartt.objects.get(pk= cartitem)
        increasecart.quantity += itemquantity
        increasecart.save ()
        messages.success(request, 'Quantity increased.')
        return redirect('mycart')

@login_required(login_url='signin')
def checkout(request):
    profile = Profile.objects.get(user__username = request.user.username)
    shopcart = Shopcartt.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for item in shopcart:
        subtotal += item.amount

    #7.5% of subtotal
    vat = 0.075 * subtotal

    total = vat + subtotal
    context ={
        'profile': profile,
        'shopcart': shopcart,
        'subtotal': subtotal,
        'vat': vat,
        'total': total,
    }
    return render(request, 'checkout.html', context)


# http://localhost:8000/completed
# payment

@login_required(login_url='signin')
def payment(request):
    if request.method == 'POST':#integrate api
        api_key= 'sk_test_d55873115b2df92ecdef230ed37e733d41e3b26a'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://34.227.27.104/completed'
        ref_code = str(uuid.uuid4())
        user = User.objects.get(username = request.user.username)
        email = user.email
        profile = Profile.objects.get(user__username =request.user.username)
        cart_code = profile.id
        total = float(request.POST['total']) * 100
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        phone = request.POST['phone']
        city = request.POST['city']
        address = request.POST['address']
        new_email = request.POST['email']

        headers ={'Authorization': f'Bearer {api_key}'}
        data ={'reference':ref_code, 'amount': int(total),'order_number': cart_code, 'email': email, 'callback_url': cburl, 'currency': 'NGN'}

        try: # make call to paystack
            r = requests.post(curl, headers=headers, json=data)# pip install requests
        except Exception:
            messages.error(request, 'network busy, refresh and try again')
        else:
            transback = json.loads(r.text)#import json, import request
            rurl = transback['data']['authorization_url']

            account = Paymentt()
            account.user = user
            account.first_name = fname
            account.last_name = lname
            account.phone = phone
            account.city = city
            account.address = address
            account.total = total/100
            account.cart_code = cart_code
            account.pay_code = ref_code
            account.paid = True
            account.save()


            email = EmailMessage(
                'Order confirmation',#title
                f'Dear{fname} , your order is confirmed! \n Your delivery is in one hour. \n Thank you for your patronage.',#content
                settings.EMAIL_HOST_USER, #company email
                [new_email]#client
            )
           
            email.fail_silently = True
            email.send()



            return redirect(rurl)
    return redirect('checkout')


def completed(request):
    profile_data = Profile.objects.get(user__username = request.user.username)
    cart = Shopcartt.objects.filter(user__username = request.user.username, paid= False)

    for item in cart:
        item.paid = True
        item.save()

        stock = Dish.objects.get(pk = item.dish.id)
        stock.max -= item.quantity
        stock.save()

    context = {
        'profile_data':profile_data,
    }
    return render(request,'completed.html', context)

