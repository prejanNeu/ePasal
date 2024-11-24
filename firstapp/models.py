from django.db import models
from django.contrib.auth.models import User  # Assuming you'll link to Django's User model

# Model for storing roles (either 'buyer' or 'seller')
class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('buyer', 'buyer'), ('seller', 'seller')])

    def __str__(self):
        return f"{self.user.email} - {self.role}"

# Model for seller information
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.company_name

# Model for buyer information
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default=None)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

# Model for products, with a foreign key to the seller
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Model for orders, linking products to buyers and sellers
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"
