from django.db import models
from django.contrib.auth.models import User

###### env environment name 
# Create your models here.

STATE_CHOICES = (
    ('Assam','Assam'),
    ('Punjab','Punjab'),
    ('Jammu and kashmir','Jammu and kashmir'),
    ('Himachal','Himachal'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=40)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length= 2)
    product_image = models.ImageField(upload_to = 'producting')

    def __str__(self):
        return str(self.title)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantiy = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_coast(self):
        return self.quantiy * self.product.discounted_price
    
STATUS_CHOICES = (
    ('Pending','Pending'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantiy = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES,default='Pending',max_length=40)


    def __str__(self):
        return str(self.id)
    
    @property
    def total_coast(self):
        return self.quantiy * self.product.discounted_price
