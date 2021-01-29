from django.conf import settings
from django.db import models

# Create your models here.


class Teachers(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60,unique=True,null=False,blank=False)
    last_name = models.CharField(max_length=30,null=True)
    first_name = models.CharField(max_length=30,null=True)
    phone = models.CharField(max_length=30,null=True,blank=True)
    image = models.ImageField(upload_to='media/',null=True,blank=True)
    status = models.SmallIntegerField(null=True)
    room_number =  models.CharField(max_length=30,null=True,blank=True)
    subjects = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.email

