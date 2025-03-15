from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import datetime, timedelta
from .models import *


def index(request):
    products = Product.objects.all()
    return render(request, "index.html", {"product": products}) 

def product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'product.html', {'product': product})


def usersignup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confpassword') 
        
        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully!")
            return redirect('userlogin') 

    return render(request, "register.html")

def userlogin(request):
    if 'username' in request.session:
        return redirect('index')  
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            if user.is_superuser:
                return redirect('firstpage')
            return redirect('index')           
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'userlogin.html')


def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect('userlogin')


def verifyotp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        otp1 = request.session.get('otp')
        otp_time_str = request.session.get('otp_time')

        if otp_time_str:
            otp_time = datetime.fromisoformat(otp_time_str)  
            otp_expiry_time = otp_time + timedelta(minutes=5)  
            if datetime.now() > otp_expiry_time:
                messages.error(request, 'OTP has expired. Please request a new one.')
                del request.session['otp']
                del request.session['otp_time']
                return redirect('verifyotp') 

        if otp == otp1:
            del request.session['otp']
            del request.session['otp_time']
            return redirect('passwordreset')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    otp = ''.join(random.choices('123456789', k=6))
    request.session['otp'] = otp
    request.session['otp_time'] = datetime.now().isoformat()

    message = f'Your email verification code is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.session.get('email')]
    send_mail('Email Verification', message, email_from, recipient_list)

    return render(request, "otp.html")


def getusername(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['email'] = user.email
            return redirect('verifyotp')
        except User.DoesNotExist:
            messages.error(request, "Username does not exist.")
            return redirect('getusername')

    return render(request, 'getusername.html')


def passwordreset(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confpassword')

        if confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        else:
            email = request.session.get('email')
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                del request.session['email']
                messages.success(request, "Your password has been reset successfully.")

                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)

                return redirect('userlogin') 
            except User.DoesNotExist:
                messages.error(request, "No user found with that email address.")
                return redirect('getusername') 

    return render(request, "passwordreset.html")





def category(request):
    return render(request, 'category.html')


def bookings(request):
    return render(request, 'bookings.html')


def delete_g(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('firstpage')

def edit_g(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        # Fetching form data
        name = request.POST.get('name')  # Fixing field name here
        colour = request.POST.get('colour')
        price = request.POST.get('price')
        offerprice = request.POST.get('offerprice')
        review = request.POST.get('review')
        description = request.POST.get('description')
        gender_id = request.POST.get('gender')
        brand_id = request.POST.get('brand')
        type_id = request.POST.get('type')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')  # For the image upload

        if name and colour and price and offerprice and review and description and gender_id and brand_id and type_id and quantity:
            product.name = name
            product.colour = colour
            product.price = price
            product.offerprice = offerprice
            product.review = review
            product.description = description
            product.gender = Gender.objects.get(id=gender_id)
            product.brand = Brand.objects.get(id=brand_id)
            product.type = Type.objects.get(id=type_id)
            product.quantity = quantity

            # If an image is uploaded, update it
            if image:
                product.image = image

            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect('firstpage')

        else:
            messages.error(request, "All fields must be filled out.")

    return render(request, 'add.html', {
        'data1': product,
        'genders': Gender.objects.all(),
        'brands': Brand.objects.all(),
        'types': Type.objects.all()
    })

# Add a New Product
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('todo')
        colour = request.POST.get('colour')
        price = request.POST.get('price')
        offerprice = request.POST.get('offerprice')
        review = request.POST.get('review')
        description = request.POST.get('description')
        gender_id = request.POST.get('gender')
        brand_id = request.POST.get('brand')
        type_id = request.POST.get('type')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')

        if name and colour and price and offerprice and review and description and gender_id and brand_id and type_id and quantity and image:
            obj = Product.objects.create(
                name=name, colour=colour, price=price, offerprice=offerprice,
                review=review, description=description, gender_id=Gender.objects.get(id=gender_id),
                brand_id=Brand.objects.get(id=brand_id), type_id=Type.objects.get(id=type_id),
                quantity=quantity, image=image
            )
            obj.save()  # Fixed this line by adding parentheses.
            return redirect('firstpage')

        messages.error(request, "All fields must be filled out.")

    return render(request, 'add.html')

# First Page (Product Listing)
def first_page(request):
    products = Product.objects.all()
    return render(request, 'firstpage.html', {'products': products})
