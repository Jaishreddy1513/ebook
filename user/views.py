from django.shortcuts import render,redirect
from .models import User,Custom_User,UserVerification,User_like_book,ResetPwVerification
from author.models import BookPublished,BooksDownload
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def send_email(recipient_email,otp):
    subject = 'Welcome to Our Website!'
    message = f'Continue by using {otp} this OTP'
    from_email = settings.DEFAULT_FROM_EMAIL # Uses the default from settings.py
    recipient_list = [recipient_email] # Must be a list

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



def home(request):
    return render(request,"home.html")



def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if User.objects.filter(user_details=email):
                messages.error(request,"Email already exist")
                return render(request,"signup.html")
            else:
                if confirm_password == password:
                    user_data = Custom_User.objects.create_customer(user_name=name,email=email,password=password)
                    user = User.objects.get(user_details=user_data)
                    messages.success(request, 'Created successfully.')
                    return redirect("verification",id=user.user_id)
                else:
                    messages.error(request,"Check password and confirm password")
                    return render(request,"signup.html",)
    return render(request,"signup.html")



def verification_user(request,id):
    try:
        user = User.objects.get(user_id=id)
        otp = UserVerification.objects.get(user_data=user)
        send_email(user.user_details,otp.otp)
        if not user.user_details.is_verified:
            if request.method == "POST":
                userverification = UserVerification.objects.get(user_data=id)
                otp = request.POST.get("otp")
                if userverification.otp == int(otp):
                    user_data=Custom_User.objects.get(email=user.user_details)
                    user_data.is_verified = True
                    user_data.save()
                    userverification.delete()
                    messages.success(request, 'User Verified')
                    return redirect("login")
                else:
                    messages.error(request,"Invalid OTP")
                    return render(request,"verification.html")
        else:
            return redirect("login")
    except User.DoesNotExist:
        return redirect("signup")
    except UserVerification.DoesNotExist:
        return redirect("signup")
    return render(request,"verification.html")




def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(email=email,password=password)
            if user is not None:
                if user.is_user:
                    try:
                        user_data = User.objects.get(user_details=user)
                    except User.DoesNotExist:
                        return redirect("author-dashboard")
                    if user.is_verified:
                        auth_login(request,user)
                        return redirect("dashboard")
                    else:
                        return redirect("verification",id=user_data.user_id)
                else:
                    messages.error(request,"It is for only for User")
                    return render(request,"login.html")
            else:
                try:
                    user_getting = User.objects.get(user_details=email)
                    messages.error(request,"Check password")
                    return render(request,"login.html")
                except User.DoesNotExist:
                    messages.error(request,"Create account")
                    return render(request,"login.html")
        return render(request,"login.html")
    
    

@login_required(login_url="login")
def dashboard(request):
    user=User.objects.get(user_details=request.user)
    books=BookPublished.objects.all()
    liked_list = User_like_book.objects.filter(user_id=user).values_list("book_id",flat=True)
    return render(request,"dashboard.html",{"books":books,"liked_list":liked_list})



@login_required(login_url="login")
def like_book(request,id):
    user = User.objects.get(user_details=request.user)
    book =BookPublished.objects.get(book_id=id)
    data = BookPublished.objects.filter(book_id=id)
    if data:
        User_like_book.objects.create(user_id=user,book_id=book)
    messages.success(request, 'Book like')
    destination = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(destination)


@login_required(login_url="login")
def unlike_book(request,id):
    user = User.objects.get(user_details=request.user)
    book =BookPublished.objects.get(book_id=id)
    like=User_like_book.objects.get(user_id=user,book_id=book)
    like.delete()
    messages.success(request, 'Book Unlike')
    destination = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(destination)



@login_required(login_url="login")
def view_book(request,id):
    user=User.objects.get(user_details=request.user)
    liked_list = User_like_book.objects.filter(user_id=user).values_list("book_id",flat=True)
    book = BookPublished.objects.filter(book_id=id)
    return render(request,"view.html",{"book":book[0],"liked_list":liked_list})

@login_required(login_url="login")
def liked_books(request):
    user=User.objects.get(user_details=request.user)
    liked_list = User_like_book.objects.filter(user_id=user)
    return render(request,"liked_books.html",{"liked_list":liked_list})



@login_required(login_url="login")
def genre(request,genre):
    genres=genre.upper()
    books=BookPublished.objects.filter(book_genres=genres)
    return render(request,"genre.html",{"books":books})


@login_required(login_url="login")
def download_book(request,id):
    user=User.objects.get(user_details=request.user)
    book = BookPublished.objects.get(book_id=id)
    if not BooksDownload.objects.filter(user_id=user,book_id=book):
        BooksDownload.objects.create(user_id=user,book_id=book)
        book.book_download+=1
        book.save()
        return redirect(f"/media/{book.book_pdf}/")
    else:
        return redirect(f"/media/{book.book_pdf}/")


@login_required(login_url="login")
def logout_user(request):
    auth_logout(request)
    messages.success(request, 'Logout')
    return redirect("login")



def forgot_password(request):
    if request.method == "POST":
        email_id = request.POST.get("email")
        try:
            user=User.objects.get(user_details=email_id)
            user_send = ResetPwVerification.objects.filter(user_id=user)
            if not user_send:
                email=ResetPwVerification.objects.create(user_id=user)
                Reset_send_email(email_id,f"http://127.0.0.1:8000/reset_password/{str(email)}")
                return redirect("login")
            else:
                print(user_send[0])
                Reset_send_email(email_id,f"http://127.0.0.1:8000/author/reset_password/{user_send[0]}")
                return redirect("author-login")
        except User.DoesNotExist:
            return redirect("signup")
    return render(request,"forgot_password.html")

def reset_password(request,id):
    try:
        user_id = ResetPwVerification.objects.get(pw_id=id)
        user_data = User.objects.get(user_details__email=user_id.user_id)
        user = Custom_User.objects.get(email=user_data)
        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                user.set_password(password)
                user.save()
                user_id.delete()
                messages.success(request,"Password reset successfull")
                return redirect("login")

            else:
                messages.error(request,"Check password")
                return redirect("reset_password",id=id)
            
    except ResetPwVerification.DoesNotExist:
       return HttpResponse("This link has been expired")
    return render(request,"reset_password.html")