from django.db import models
from django.forms import widgets

# Create your models here.

class UserAccount(models.Model):
    full_name = models.CharField(max_length=256)
    gender = models.CharField(max_length=256)
    contact_number = models.CharField(max_length=256)
    email_address = models.EmailField(max_length=256)
    home_address = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    status = models.CharField(max_length=256, null= True, blank= True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.contact_number