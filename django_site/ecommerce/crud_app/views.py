from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from.models import Category, Product, Cart, Order
from.forms import OrderForm

def main_page(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.get(id=customer_id)
        return render(request,'main.html',{'customer': customer})
    else:
        return redirect('login')

def home(request):
    categories = Category.objects.all()
    return render(request,'home.html',{'categories':categories})

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
        except Customer.DoesNotExists:
            messages.error(request,"Invalid username or password")
    return render(request,'login.html')



def logout_view(request):
    logout(request)
    return redirect('login')

def product_list(request,category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.all()
    return render(request,'product_list.html',{'products':products})

def view_products(request,category_id):
    category=Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    context = {'category': category,'products': products,}
    return render(request,'view_products.html',context)

def product_detail(request, cname,pname):
    category = Category.objects.get(name=cname)
    product = Product.objects.get(name=pname,category=category)
    return render(request,'product_detail.html',{'product':product})

def add_to_cart(request,product_id):
    from.models import Customer
    if request.session.get('customer_id'):
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(id=customer_id)
        user = customer
        product = get_object_or_404(Product,id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request,"Quantity updated in your cart.")
        else:
            messages.success(request,"Product added to your cart.")
        return redirect('product_detail',cname=product.category.name,pname=product.name)
    else:
        return redirect('login')

def view_cart(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.get(id=customer_id)
        user = customer
        cart_items = Cart.objects.filter(user=user)
        total = sum(item.total_price()for item in cart_items)
        return render(request,'view_cart.html',{'cart_items':cart_items,'total':total})
    else:
        return redirect('login')

def place_order(request,customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            cart = request.session.get('cart',[])
            products = Product.objects.filter(id_in=cart)
            total = sum(p.price for p in products)
            request.session['cart']=[]
            return render(request,'order_success.html',{
                'order': order,
                'products': products,
                'total': total})
    else:
        form = OrderForm()
    return render(request,'order.html',{'form':form})

def order_success(request):
    return render(request,'order_success.html')
    


# Create your views here.
