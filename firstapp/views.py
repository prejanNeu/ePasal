from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product


def home_page(request):
    return render(request,"firstapp/home.html")

@login_required(login_url='login_page')
def buyer_dashboard(request):
    
    return render(request,'firstapp/buyer_dashboard.html')


def product_page(request):
    products = Product.objects.all()

    return render(request,'firstapp/product.html',{'products':products})
def register_page(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')

        user = User.objects.create_user(username=email)
        user.set_password(password)

        user.save()
        return redirect('login_page')

    return render(request,"firstapp/register.html")


def login_page(request):

    if request.method == "POST":
    
        username = request.POST.get('email')
        password = request.POST.get('password')


        user = authenticate(username=username,password=password)
        print(user,username,password)
        if user is not None:
            login(request,user)
            return redirect('buyer_dashboard')
        
        else:
            return HttpResponse("invalid username or password")


    return render(request,"firstapp/login.html")