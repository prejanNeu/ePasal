from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product,UserRole,Seller,Buyer
from .utils import generateOtp,sendEmail


def get_code(request):
    email = request.session.get("email")
    otp = generateOtp()
    sendEmail(email,otp)
    request.session['otp'] = otp
    return redirect("veryfy_email")


def veryfy_email(request):
    email = request.session.get('email')
    password = request.session.get('password')
    role = request.session.get("role")
    otp = request.session.get('otp')
    

    if request.method == "POST":
        get_otp = request.POST.get("otp")
        print(otp,get_otp)
        if otp == get_otp:
            
            if role == "seller":
                return redirect("seller_register")
            
            if role == "buyer":
                return redirect("buyer_dashboard")

        else:
            return render(request,"firstapp/veryfyEmail.html",{"message":"envalid otp "})
        
    return render(request,"firstapp/veryfyEmail.html")
    


def home_page(request):
    return render(request,"firstapp/home.html")

def seller_register(request):
    email = request.session.get('email')
    password = request.session.get('password')

    if not email or not password:
        return HttpResponse("Session expired or invalid data. Please register again.")
    
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        contact_number = request.POST.get('contact_number')
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        
        # Create a seller
        seller = Seller.objects.create(user=user, company_name=company_name, contact_number=contact_number)
        seller.save()

        # Assign a role
        user_role = UserRole.objects.create(user=user, role='seller')
        user_role.save()
        
        return redirect('login_page')  # Redirect email verification page 

    return render(request, 'firstapp/seller_register.html')


def buyer_register(request):
    email = request.session.get('email')
    password = request.session.get('password')


    if not email or not password:
        return HttpResponse("Session expired or invalid data. Please register again.")
    
    if request.method=="POST":

        name = request.POST.get("name")
        address = request.POST.get("address")
        contact_number= request.POST.get("contact_number")

        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        buyer = Buyer.objects.create(user=user, name=name,address=address, contact_number=contact_number)
        buyer.save()





@login_required(login_url='login_page')
def buyer_dashboard(request):
    
    return render(request,'firstapp/buyer_dashboard.html')


@login_required(login_url='login_page')
def seller_dashboard(request):
    seller = Seller.objects.filter(user=request.user).first()


    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        seller = Seller.objects.get(user=request.user)

        product = Product.objects.create(name=name,description=description,price=price,image=image,seller=seller)
        product.save()

    return render(request,'firstapp/seller_dashboard.html',{"seller":seller})


def product_page(request):
    products = Product.objects.all()

    return render(request,'firstapp/product.html',{'products':products})


def register_page(request):

    if request.method == "POST":

        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')

        request.session['email'] = email
        request.session['password'] = password
        request.session['role'] = role
       
        

        return redirect("get_code")


    return render(request,"firstapp/register.html")


def login_page(request):

    if request.method == "POST":
    
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        print(user,username,password)
        if user is not None:
            user_role = UserRole.objects.get(user=user)
            role = user_role.role
            if role =="buyer":
                login(request,user)
                return redirect('buyer_dashboard')
            
            elif role == "seller":
                login(request,user)
                return redirect('seller_dashboard')
        
        else:
            return HttpResponse("invalid username or password")


    return render(request,"firstapp/login.html")