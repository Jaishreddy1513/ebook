from django.urls import path
from user import views

urlpatterns = [
    path('', views.home ,name="home"),
    path('signup/', views.signup ,name="signup"),
    path('login/', views.login ,name="login"),
    path('dashboard/', views.dashboard ,name="dashboard"),
    path('verification_user/<str:id>/', views.verification_user ,name="verification"),
    path('view_book/<str:id>/', views.view_book ,name="user_view_book"),
    path('genre/<str:genre>/', views.genre ,name="genre"),
    path('liked_book/<str:id>/', views.like_book ,name="like_book"),
    path('unlike_book/<str:id>/', views.unlike_book ,name="unlike_book"),
    path('liked_books/', views.liked_books ,name="liked_books"),
    path('download_book/<str:id>/', views.download_book ,name="user_download_book"),
    path('logout/', views.logout_user ,name="logout"),
]