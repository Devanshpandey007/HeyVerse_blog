from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .baseManager import UserManager



# Create your models here.

class User (AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True)
    avatar = models.URLField(default="", blank=True)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()  
    image = models.URLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    
