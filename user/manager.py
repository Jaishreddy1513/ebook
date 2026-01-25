
from user import models
from author.models import Author,AuthorVerification
from django.contrib.auth.models import BaseUserManager
import random

class UserManager(BaseUserManager):
    def create_user(self,email="",password=""):
        if not email:
            raise ValueError("enter your email")
        if not password:
            raise ValueError("enter your password")
        
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password):
        user = self.create_user(email=email,password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_customer(self,user_name,email,password):
        user = self.create_user(email=email,password=password)
        user.is_user = True
        user.save(using=self._db)
        make_user = models.User.objects.create(user_name=user_name,user_details=user)
        models.UserVerification.objects.create(user_data=make_user,otp=random.randint(1000,10000))
        return user
    
    def create_author(self,author_name,email,password):
        user = self.create_user(email=email,password=password)
        user.is_author = True
        user.save(using=self._db)
        make_user = Author.objects.create(author_name=author_name,author_details=user)
        AuthorVerification.objects.create(author_data=make_user,otp=random.randint(1000,10000))
        return user
