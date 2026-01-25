# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# import uuid
# from .manager import UserManager
# # Create your models here.

# class Custom_User(AbstractBaseUser,PermissionsMixin):
#     email = models.EmailField(max_length=254,primary_key=True)
#     password = models.CharField(null=False)
    
    
#     is_user = models.BooleanField(default=False)
#     is_author = models.BooleanField(default=False)
#     is_verified = models.BooleanField(default=False)
    
    
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
    
#     USERNAME_FIELD="email"
#     REQUIRED_FIELDS = []
#     objects = UserManager()
    
    
#     def __str__(self):
#         return self.email
    
    
# class User(models.Model):
#     user_id = models.UUIDField(default=uuid.uuid4,primary_key=True)
#     user_name = models.CharField(max_length=150,null=False)
#     user_details = models.OneToOneField("user.Custom_User", on_delete=models.CASCADE)
#     user_created = models.DateField(auto_now_add=True)
    
#     def __str__(self):
#         return self.user_details.email
    
    
# class UserVerification(models.Model):
#     user_data = models.OneToOneField("user.User",primary_key=True,on_delete=models.CASCADE)
#     otp = models.IntegerField()
    
#     def __str__(self):
#         return self.user_data.email