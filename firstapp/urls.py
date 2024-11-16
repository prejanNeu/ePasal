from django.urls import path 
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.home_page,name="home_page"),
    path("register/",views.register_page,name="register_page"),
    path("login/",views.login_page,name="login_page"),
    path("product/",views.product_page,name='product_page'),
    path('buyer_dashboard',views.buyer_dashboard,name='buyer_dashboard'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
