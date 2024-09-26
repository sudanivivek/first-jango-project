from django.db import models

# Create your models here.
class Register(models.Model):
  username = models.CharField(max_length=150, unique=True)
  email = models.EmailField()
  firstname= models.CharField(max_length=30)
  lastname= models.CharField(max_length=30)
  password = models.CharField(max_length=20)
  address = models.CharField(max_length=255, blank=True, null=True)
  phone_number = models.CharField(max_length=12, blank=True, null=True)

def __str__(self):
        return self.username  