from django.db import models

from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self,email,first_name=None,last_name=None,password=None):
        if not email:
            raise ValueError("Email is required")
        
        email=self.normalize_email(email=email)

        user=self.model(email=email,first_name=first_name,last_name=last_name)
        
        user.is_active=True
        user.is_staff=False
        user.set_password(password)

        user.save(using=self._db)

        return user
    

    def create_superuser(self,email,first_name=None,last_name=None,password=None):
        
        user=self.create_user(email,first_name,last_name,password)

        user.is_active=True
        user.is_superuser=True
        user.is_staff=True

        user.save(using=self._db)
        return user
    



class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True,max_length=255)
    first_name=models.CharField(max_length=255,blank=True,null=True)
    last_name=models.CharField(max_length=255,blank=True,null=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]
    objects=UserManager()

    def __str__(self):
        return self.email
    
    def save(self,*args,**kwargs):
        if not self.first_name:
            self.first_name=self.email
        
        super().save(*args,**kwargs)

        

        
