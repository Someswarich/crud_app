from django.db import models
# from cloudinary.models import CloudinaryField


# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=30,default='null')
    description=models.CharField(max_length=50,default='No description')
    price=models.IntegerField()
    # photo = CloudinaryField('image')

