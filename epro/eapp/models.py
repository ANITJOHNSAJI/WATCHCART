from django.db import models

class Product(models.Model):
    GENDER_CHOICES = [
        (True, 'Female'),
        (False, 'Male'),
        (None, 'Unisex'),
    ]
    
    TYPE_CHOICES = [
        (True, 'Analogue'),
        (False, 'Digital'),
        (None, 'Analogue/Digital'),
    ]

    name = models.CharField(max_length=255)
    colour = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offerprice = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    gender = models.BooleanField(choices=GENDER_CHOICES, null=True, blank=True)
    type = models.BooleanField(choices=TYPE_CHOICES, null=True, blank=True)
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
