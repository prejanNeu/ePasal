from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from .models import Product,UserRole,Seller,Buyer,Cart
from .utils import generateOtp,sendEmail
import json 



# get otp in the email 
def get_code(request):
    email = request.session.get("email")
    otp = generateOtp()
    sendEmail(email,otp)
    request.session['otp'] = otp
    return redirect("veryfy_email")


# veryfy with otp 
def veryfy_email(request):
    email = request.session.get('email')
    password = request.session.get('password')
    role = request.session.get("role")
    otp = request.session.get('otp')
    

    if request.method == "POST":
        get_otp = request.POST.get("otp")
        
        if otp == get_otp:
            
            if role == "seller":
                return redirect("seller_register")
            
            if role == "buyer":
                return redirect("buyer_register")

        else:
            return render(request,"firstapp/veryfyEmail.html",{"message":"envalid otp "})
        
    return render(request,"firstapp/veryfyEmail.html")
    

# this is the home page of the web page 
def home_page(request):
    return render(request,"firstapp/home.html")


# this is the page for the seller register 
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
        
        return redirect('buyer_register')  # Redirect email verification page 

    return render(request, 'firstapp/seller_register.html')

# this is the page for the buyer register
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

        user_role = UserRole.objects.create(user=user, role='buyer')
        user_role.save()

        return redirect("login_page")

    return render(request,"firstapp/buyer_register.html")




# buyer dashboard page 
@login_required(login_url='login_page')
def buyer_dashboard(request):

    userrole = UserRole.objects.filter(user=request.user).first()
    role = userrole.getRole()

    if role == "buyer":
        cart_items = Cart.objects.filter(user=request.user)
        buyer = Buyer.objects.filter(user=request.user).first()  # Assuming one buyer per user
        context = {
            'buyer': buyer,
            'cart_items': cart_items,
        }

    else:
        return redirect("login_page")

    return render(request, 'firstapp/buyer_dashboard.html', context)



# seller dashboard page

def seller_dashboard(request):

    userrole = UserRole.objects.filter(user=request.user).first()
    role = userrole.getRole()

    if role == "seller":
        seller = Seller.objects.filter(user=request.user).first()


        if request.method == "POST":
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            image = request.FILES.get('image')

            seller = Seller.objects.get(user=request.user)

            product = Product.objects.create(name=name,description=description,price=price,image=image,seller=seller)
            product.save()

    else:
        return redirect("login_page")

    return render(request,'firstapp/seller_dashboard.html',{"seller":seller})

# the page where the product are displaying 
def product_page(request):
    products = Product.objects.all()

    return render(request,'firstapp/product.html',{'products':products})



# the page for register the new user 
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



# this is the login page for the user 
def login_page(request):

    if request.method == "POST":
    
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            user_role = UserRole.objects.get(user=user)
            role = user_role.role

            login(request,user)

            if role =="buyer":
                return redirect('buyer_dashboard')
            
            elif role == "seller":
                print(role)
                print("\n")
                return redirect('seller_dashboard')
        
        else:
            return HttpResponse("invalid username or password")


    return render(request,"firstapp/login.html")




# after adding item to the cart 
@login_required
def add_to_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data from the request body
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)  # Default quantity to 1
            print(product_id)
            # Ensure the product exists
            product = get_object_or_404(Product, id=product_id)

            # Add product to the user's cart
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                # If the item is already in the cart, update the quantity
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({'status': 'success', 'message': f'{product.name} added to cart.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



# This is page log out it hit when the user do logout 
def logout_page(request):
    # Ensure the user is logged in before attempting to log out
    if request.user.is_authenticated:
        logout(request)  # This will log the user out and clear their session
        return redirect('login_page')  # Redirect to the login page after logging out
    else:
        return redirect('login_page')

# hit when the user delte the item from the cart 
def delete_product(request):
    ...



def dashboard(request):
    if request.user.is_authenticated:
        user_role = UserRole.objects.filter(user=request.user).first()
        # print(request.user)
        if user_role:
            role = user_role.getRole()
            if role == "buyer":
                return redirect("buyer_dashboard")
            elif role == "seller":
                # Sweet error message for seller trying to buy
                messages.error(request, "Oops! You're a seller, so you can't make purchases here. Please use your buyer account for that.")
                return redirect("seller_dashboard")
        else:
            # Sweet error message when role is not found
            messages.error(request, "Whoops! We couldn't find your role. Please check your account settings.")
            return redirect("product_page")
    else:
        # Sweet error message for unauthenticated user
        messages.error(request, "Uh-oh! It looks like you're not logged in. Please log in to continue.")
        return redirect("login_page")


