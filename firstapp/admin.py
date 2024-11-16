from django.contrib import admin
from .models import Product, Seller, Buyer, UserRole, Order

# Product Admin Configuration
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'seller', 'image')  # Fields to display in the list view
    search_fields = ('name', 'description', 'price', 'seller__company_name')  # Searchable fields
    list_filter = ('seller', 'price')  # Filter options

admin.site.register(Product, ProductAdmin)

# Seller Admin Configuration
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'contact_number')  # Fields to display in the list view
    search_fields = ('user__username', 'company_name')  # Searchable fields
    list_filter = ('company_name',)

admin.site.register(Seller, SellerAdmin)

# Buyer Admin Configuration
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'contact_number')  # Fields to display in the list view
    search_fields = ('user__username', 'address')  # Searchable fields
    list_filter = ('user__username',)

admin.site.register(Buyer, BuyerAdmin)

# UserRole Admin Configuration
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')  # Fields to display in the list view
    search_fields = ('user__email', 'role')  # Searchable fields

admin.site.register(UserRole, UserRoleAdmin)

# Order Admin Configuration
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'buyer', 'order_date', 'status')  # Fields to display in the list view
    search_fields = ('product__name', 'buyer__user__username')  # Searchable fields
    list_filter = ('status', 'order_date')  # Filter options

admin.site.register(Order, OrderAdmin)
