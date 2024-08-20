from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    breed = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    age = models.IntegerField()
    petimage = models.ImageField(upload_to='images',default=0)

#django by default assigns id which will be foreign key in cart 

class Cart(models.Model):
    pid = models.ForeignKey(Pet,on_delete=models.CASCADE, db_column='pid')
    uid = models.ForeignKey(User, on_delete=models.CASCADE ,db_column='uid')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
class Order(models.Model):
    orderid = models.IntegerField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE ,db_column='uid')
    pid = models.ForeignKey(Pet,on_delete=models.CASCADE, db_column='pid')
    quantity = models.IntegerField()