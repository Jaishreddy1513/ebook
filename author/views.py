from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Author,BookPublished,AuthorVerification,BooksDownload,ResetPwVerification
from user.models import Custom_User,User
# from django.http import HttpRe

from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def send_email(recipient_email,otp):
    subject = 'Welcome to Our Website!'
    message = f'Continue by using {otp} this OTP'
    from_email = settings.DEFAULT_FROM_EMAIL 
    recipient_list = [recipient_email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

def Reset_send_email(recipient_email,reset_link):
    subject = 'Welcome to Our Website!'
    message = f'Click the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email.'
    from_email = settings.DEFAULT_FROM_EMAIL # Uses the default from settings.py
    recipient_list = [recipient_email] # Must be a list

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

def sigup_author(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if Author.objects.filter(author_details=email):
            messages.error(request,"Email already exist")
            return render(request,"author_signup.html")
        else:
            if confirm_password == password:
                user_data = Custom_User.objects.create_author(author_name=name,email=email,password=password)
                user = Author.objects.get(author_details=user_data)
                messages.success(request, 'Created successfully.')
                return redirect("author-verification",id=user.author_id)
            else:
                messages.error(request,"Check password and confirm password")
                return render(request,"author_signup.html")
    return render(request,"author_signup.html")



def verification_author(request,id):
    try:
        user = Author.objects.get(author_id=id)
        otp = AuthorVerification.objects.get(author_data=user)
        send_email(user.author_details,otp.otp)
        if not user.author_details.is_verified:
            if request.method == "POST":
                userverification = AuthorVerification.objects.get(author_data=id)
                otp = request.POST.get("otp")
                if userverification.otp == int(otp):
                    user_data=Custom_User.objects.get(email=user.author_details)
                    user_data.is_verified = True
                    user_data.save()
                    userverification.delete()
                    messages.success(request, 'User Verified')
                    return redirect("author-login")
                else:
                    messages.error(request,"Invalid OTP")
                    return render(request,"verification.html")
        else:
            return redirect("author-login")
    except Author.DoesNotExist:
        return redirect("author-signup")
    except AuthorVerification.DoesNotExist:
        return redirect("author-signup")
    return render(request,"verification.html")


def login_author(request):
    if request.user.is_authenticated:
        return redirect("author-dashboard")
    else:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(email=email,password=password)
            if user is not None:
                try:
                    user_data = Author.objects.get(author_details=user)
                except Author.DoesNotExist:
                    return redirect("dashboard")
                if user.is_verified:
                    if user.is_author:
                        auth_login(request,user)
                        messages.success(request, 'User Login')
                        return redirect("author-dashboard")
                    else:
                        messages.error(request,"It is for only for User")
                        return render(request,"author_login.html")
                else:
                    messages.error(request,"Check password")
                    return redirect("author-verification",id=user_data.author_id)
            else:
                try:
                    user_getting = Author.objects.get(author_details=email)
                    messages.error(request,"Check password")
                    return render(request,"author_login.html")
                except Author.DoesNotExist:
                    messages.error(request,"Create account")
                    return render(request,"author_login.html")
        return render(request,"author_login.html")


  
@login_required(login_url="author-login")  
def author_dashboard(request):
    author=Author.objects.get(author_details=request.user)
    book = BookPublished.objects.filter(author_id=author)
    downloads=0
    for i in book:
        downloads+=i.book_download
    return render(request,"author_dashboard.html",{"books":book,"published":author.number_of_book_published,"downloads":downloads})



@login_required(login_url="author-login")
def create_book(request):
    author=Author.objects.get(author_details=request.user)
    if request.method == "POST":
        book_name=request.POST.get("book_name")
        book_title=request.POST.get("book_title")
        book_description=request.POST.get("book_description")
        book_genres=request.POST.get("book_genres")
        book_cover_page=request.FILES.get("book_cover_page")
        book_pdf=request.FILES.get("book_pdf")
        book = BookPublished.objects.create(book_name=book_name,author_id=author,book_title=book_title,book_description=book_description,book_genres=book_genres,book_cover_page=book_cover_page,book_pdf=book_pdf)
        author=Author.objects.get(author_id=author.author_id)
        author.number_of_book_published +=1
        author.save()
        messages.success(request, 'Book Create')
        return redirect("author-dashboard")
    return render(request,"author_book_create.html")



@login_required(login_url="author-login")
def view_book(request,id):
    author=Author.objects.get(author_details=request.user)
    book = BookPublished.objects.filter(author_id=author,book_id=id)
    return render(request,"author_view.html",{"book":book[0]})

@login_required(login_url="author-login")
def edit_book(request,id):
    book = BookPublished.objects.get(book_id=id)
    author=Author.objects.get(author_details=request.user)
    if book.author_id.author_id == author.author_id:
        if request.method == "POST":
            book.book_name=request.POST.get("book_name")
            book.book_title=request.POST.get("book_title")
            book.book_description=request.POST.get("book_description")
            book.book_genres=request.POST.get("book_genres")
            book.book_cover_page=request.FILES.get("book_cover_page",book.book_cover_page)
            book.book_pdf=request.FILES.get("book_pdf",book.book_pdf)
            book.save()
            messages.success(request, 'Book Updata')
            return redirect("author-dashboard")
    else:
        return redirect("author-dashboard")
    return render(request,"author_edit_book.html",{"author_book":book})

@login_required(login_url="author-login")
def delete_book(request,id):
    book = BookPublished.objects.get(book_id=id)
    author=Author.objects.get(author_details=request.user)
    if book.author_id.author_id == author.author_id:
        book.delete()
        author.number_of_book_published-=1
        author.save()
        messages.success(request, 'Book Delete')
        return redirect("author-dashboard")
    else:
        return redirect("author-dashboard")
    
@login_required(login_url="author-login") 
def download_book(request,id):
    book = BookPublished.objects.get(book_id=id)
    return redirect(f"/media/{book.book_pdf}/")


@login_required(login_url="author-login")
def logout_user(request):
    auth_logout(request)
    messages.success(request,'Logout')
    return redirect("author-login")


def forgot_password(request):
    if request.method == "POST":
        email_id = request.POST.get("email")
        try:
            user=Author.objects.get(author_details=email_id)
            user_send = ResetPwVerification.objects.filter(user_id=user)
            if not user_send:
                email=ResetPwVerification.objects.create(user_id=user)
                Reset_send_email(email_id,f"http://127.0.0.1:8000/author/reset_password/{email}")
                return redirect("author-login")
            else:
                print(user_send[0])
                Reset_send_email(email_id,f"http://127.0.0.1:8000/author/reset_password/{user_send[0]}")
                return redirect("author-login")
        except Author.DoesNotExist:
            return redirect("author-signup")
    return render(request,"forgot_password.html")

def reset_password(request,id):
    try:
        user_id = ResetPwVerification.objects.get(pw_id=id)
        user_data = Author.objects.get(author_details__email=user_id.user_id)
        user = Custom_User.objects.get(email=user_data)
        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                user.set_password(password)
                user.save()
                user_id.delete()
                messages.success(request,"Password reset successfull")
                return redirect("author-login")
            else:
                messages.error(request,"Check password")
                return redirect("author-reset_password",id=id)
            
    except ResetPwVerification.DoesNotExist:
       return HttpResponse("This link has been expired")
    return render(request,"reset_password.html")