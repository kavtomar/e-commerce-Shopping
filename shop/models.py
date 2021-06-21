from django.db import models


# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.TextField(max_length=5000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")
    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default='')
    email = models.EmailField(max_length=100, default='')
    phone = models.IntegerField(default='')
    review = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class  Order(models.Model) :
    order_id =models.AutoField(primary_key = True)
    items_json = models.CharField(max_length=500)
    name = models.CharField(max_length= 100)
    email = models.EmailField(max_length= 100)
    phone = models.CharField(max_length=12, default="")
    amount = models.IntegerField(default=0)
    address = models.CharField(max_length= 500)
    city = models.CharField(max_length= 100)
    state = models.CharField(max_length= 100)
    zip_code = models.CharField(max_length= 50)

class OrderUpdate(models.Model)  :
    update_id = models.AutoField(primary_key = True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:10] + "......"