from django.urls import path 
from . import views 


urlpatterns = [
    path("",views.home_page,name="home_page"),
    path("register/",views.register_page,name="register_page"),
    path("login/",views.login_page,name="login_page"),
    path("product/",views.product_page,name='product_page'),
    path('buyer_dashboard',views.buyer_dashboard,name='buyer_dashboard'),
    path('seller_dashboard/',views.seller_dashboard,name='seller_dashboard'),
    path("seller_register",views.seller_register,name="seller_register"),
    path("veryfy_email",views.veryfy_email,name="veryfy_email"),
    path("get_code/",views.get_code,name="get_code"),
    path("add_to_cart",views.add_to_cart,name="add_to_cart"),
    path("buyer_register",views.buyer_register,name="buyer_register"),
    path("logout_page",views.logout_page,name="logout"),
    path("delete_cart",views.delete_product,name="delete_product"),
]


