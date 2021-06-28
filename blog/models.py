from django.db import models

# Create your models here.
class Blogpost(models.Model):
    post_id = models.AutoField(primary_key= True)
    title = models.CharField(max_length=100)
    head0 = models.CharField(max_length=500, default="")
    chead0 = models.CharField(max_length=5000, default="")
    thumbnail1 = models.ImageField(upload_to="shop/images", default="")
    head1 = models.CharField(max_length=500, default="")
    chead1 = models.CharField(max_length=5000, default="")
    thumbnail2 = models.ImageField(upload_to="shop/images", default="")
    head2 = models.CharField(max_length=500, default="")
    chead2 = models.CharField(max_length=5000, default="")
    thumbnail3 = models.ImageField(upload_to="shop/images", default="")
    head3 = models.CharField(max_length=500, default="")
    chead3 = models.CharField(max_length=5000, default="")
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to="shop/images", default="")
    def __str__(self):
        return self.title