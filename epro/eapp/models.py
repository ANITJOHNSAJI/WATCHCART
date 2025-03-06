from django.db import models

# Create your models here.
class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
class Product(models.Model):
    name = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery_images/')
    image1 = models.ImageField(upload_to='gallery_images/')
    image2 = models.ImageField(upload_to='gallery_images/')
    image3 = models.ImageField(upload_to='gallery_images/')
    image4 = models.ImageField(upload_to='gallery_images/')
    image5 = models.ImageField(upload_to='gallery_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offerprice = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    review = models.TextField()
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
