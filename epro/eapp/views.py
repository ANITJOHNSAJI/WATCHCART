from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import datetime, timedelta
from .models import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required



def index(request):
    # Fetch the latest 4 products by ordering them by ID in descending order
    products = Product.objects.all().order_by('-id')[:4]
    
    return render(request, "index.html", {"products": products})

def product(request, id):
    product = get_object_or_404(Product, pk=id)

    # Get cart items only if the user is authenticated
    cart_item_ids = []
    if request.user.is_authenticated:
        cart_item_ids = list(Cart.objects.filter(user=request.user).values_list('product_id', flat=True))

    return render(request, 'product.html', {
        'product': product,
        'cart_item_ids': cart_item_ids
    })

def product_list(request):
    # Fetch all products to display in the template
    products = Product.objects.all()
    return render(request, 'allproduct.html', {'products': products})

def search_results(request):
    query = request.GET.get('q')
    
    if query:
        # Filters products whose name contains the query text (case-insensitive)
        results = Product.objects.filter(name__icontains=query)
    else:
        results = Product.objects.all()  # Return all products if no query is provided

    return render(request, 'search.html', {'results': results, 'query': query})

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
    if request.user.is_authenticated:  # Instead of checking session directly
        return redirect('index')  

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('firstpage')  # Check that the 'firstpage' URL exists
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
                return redirect('verifyotp')  # Allow user to request a new OTP

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
        name = request.POST.get('name')
        colour = request.POST.get('colour')
        price = request.POST.get('price')
        offerprice = request.POST.get('offerprice')
        description = request.POST.get('description')
        gender = request.POST.get('gender')  # 'Female', 'Male', or 'Unisex'
        type = request.POST.get('type')  # 'Digital', 'Analogue', or 'Analogue/Digital'
        brand = request.POST.get('brand')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        image5 = request.FILES.get('image5')

        # Ensure gender and type are from the predefined choices
        if gender not in dict(Product.GENDER_CHOICES):
            messages.error(request, 'Invalid gender choice.')
            return redirect('edit_g', id=id)
        if type not in dict(Product.TYPE_CHOICES):
            messages.error(request, 'Invalid type choice.')
            return redirect('edit_g', id=id)

        # Update the product fields
        product.name = name
        product.colour = colour
        product.price = price
        product.offerprice = offerprice
        product.description = description
        product.gender = gender
        product.type = type
        product.brand = brand
        product.quantity = quantity

        # If images are uploaded, update them
        if image:
            product.image = image
        if image1:
            product.image1 = image1
        if image2:
            product.image2 = image2
        if image3:
            product.image3 = image3
        if image4:
            product.image4 = image4
        if image5:
            product.image5 = image5

        product.save()  # Save the updated product
        messages.success(request, "Product updated successfully!")
        return redirect('firstpage')

    return render(request, 'add.html', {
        'data1': product,
    })

# Add a New Product
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        colour = request.POST.get('colour')
        price = request.POST.get('price')
        offerprice = request.POST.get('offerprice')
        description = request.POST.get('description')
        gender = request.POST.get('gender')  # 'Female', 'Male', or 'Unisex'
        type = request.POST.get('type')  # 'Digital', 'Analogue', or 'Analogue/Digital'
        brand = request.POST.get('brand')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        image5 = request.FILES.get('image5')

        # Ensure gender and type are from the predefined choices
        if gender not in dict(Product.GENDER_CHOICES):
            messages.error(request, 'Invalid gender choice.')
            return redirect('add_product')
        if type not in dict(Product.TYPE_CHOICES):
            messages.error(request, 'Invalid type choice.')
            return redirect('add_product')

        # Create the product
        Product.objects.create(
            name=name, colour=colour, price=price, offerprice=offerprice,
            description=description, gender=gender, type=type, brand=brand, quantity=quantity,
            image=image, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5
        )
        messages.success(request, "Product added successfully!")
        return redirect('firstpage')  # Redirect to the product listing page

    return render(request, 'add.html')

@login_required(login_url='userlogin')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if cart_item.quantity < product.quantity:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{product.name} has been added to your cart.")
    else:
        messages.error(request, "Sorry, this product is out of stock.")

    return redirect('cart_view')

@login_required(login_url='userlogin')
def increment_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)

    if cart_item.quantity < cart_item.product.quantity:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Quantity updated.")
    else:
        messages.error(request, "No more stock available.")

    return redirect('cart_view')

@login_required(login_url='userlogin')
def decrement_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, "Quantity updated.")
    else:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")

    return redirect('cart_view')

@login_required(login_url='userlogin')
def delete_cart_item(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_view')

@login_required(login_url='userlogin')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required(login_url='userlogin')
def checkout(request):
    return render(request, 'checkout.html')

# First Page (Product Listing)
def first_page(request):
    products = Product.objects.all()
    return render(request, 'firstpage.html', {'products': products})

