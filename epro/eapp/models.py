from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class Product(models.Model):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Unisex', 'Unisex'),
    ]
    
    TYPE_CHOICES = [
        ('Analogue', 'Analogue'),
        ('Digital', 'Digital'),
        ('Analogue/Digital', 'Analogue/Digital'),
    ]

    name = models.CharField(max_length=255)
    colour = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offerprice = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)
    brand = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    image1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)
    image5 = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the cart to the user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link the cart item to a product (use 'Gallery' in your case)
    quantity = models.PositiveIntegerField(default=1)  # Default quantity is 1

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
    
    def get_total_price(self):
        return self.product.offerprice * self.quantity
    


    



    
