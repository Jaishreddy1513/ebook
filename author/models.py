from django.db import models
import uuid
# # Create your models here.


class Author(models.Model):
    author_id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    author_name = models.CharField(max_length=150,null=False)
    author_details = models.OneToOneField("user.Custom_User", on_delete=models.CASCADE)
    number_of_book_published = models.IntegerField(default=0,null=True)
    author_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.author_details.email
    
    
class AuthorVerification(models.Model):
    author_data = models.OneToOneField("author.Author",primary_key=True,on_delete=models.CASCADE)
    otp = models.IntegerField()
    
    def __str__(self):
        return self.author_data.email
    
    
def book_path(obj, filename):
    ext = filename.split('.')[-1]
    unique_name = f"{obj.book_id}.{ext}"
    return f"{obj.author_id.author_name}/Book_upload/{unique_name}"  

def book_pdf_path(obj, filename):
    ext = filename.split('.')[-1]
    unique_name = f"{obj.book_id}.{ext}"
    return f"{obj.author_id.author_name}/Book_pdf/{unique_name}"  
    


class BookPublished(models.Model):
    book_id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=500,null=False)
    book_title = models.CharField()
    book_description = models.CharField()
    book_genres = models.CharField(choices=[("Fiction","FICTION"),("Fantasy","FANTASY"),("Mystery","MYSTERY"),("Romance","ROMANCE"),("Biography","BIOGRAPHY"),("Technology","TECHNOLOGY"),("Business","BUSINESS"),("Self-Help","SELF-HELP")])
    book_cover_page = models.ImageField(upload_to=book_path, height_field=None, width_field=None, max_length=None)
    book_pdf = models.FileField(upload_to=book_pdf_path,null=False)
    book_download = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.author_id.author_name}-{self.book_name}-{self.book_id}"
    


class BooksDownload(models.Model):
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True, blank=True)
    book_id = models.ForeignKey("author.BookPublished", on_delete=models.CASCADE, null=True, blank=True)


class ResetPwVerification(models.Model):
    pw_id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    user_id = models.OneToOneField("author.Author",on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.pw_id}"