from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from.models import Category, Product, Customer


def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        password = request.POST['password'] 
        if Customer.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
        elif Customer.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
        else:
            Customer.objects.create(username=username,email=email,password=password)
            messages.success(request,"Registration successful")
            return redirect('login')
    return render(request,'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            customer = Customer.objects.get(username=username,password=password)
            request.session['customer_id'] = customer.id
            messages.success(request,f"welcome {customer.username}")
            return redirect('home')
        except Customer.DoesNotExist:
            messages.error(request,"Invalid username or password")
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
