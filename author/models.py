# from django.db import models
# import uuid
# # Create your models here.


# class Author(models.Model):
#     author_id = models.UUIDField(default=uuid.uuid4,primary_key=True)
#     author_name = models.CharField(max_length=150,null=False)
#     author_details = models.OneToOneField("user.Custom_User", on_delete=models.CASCADE)
#     number_of_book_published = models.IntegerField(default=0,null=True)
#     verified_by_admin = models.BooleanField(default=False)
#     author_created = models.DateField(auto_now_add=True)
    
#     def __str__(self):
#         return self.author_details.email
    
    
# class AuthorVerification(models.Model):
#     author_data = models.OneToOneField("author.Author",primary_key=True,on_delete=models.CASCADE)
#     otp = models.IntegerField()
    
#     def __str__(self):
#         return self.author_data.email
    