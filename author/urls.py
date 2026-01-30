from django.urls import path
from author import views
from user.views import home

urlpatterns = [
    path('author/', home ,name="home"),
    path('author/signup/', views.sigup_author ,name="author-signup"),
    path('author/login/', views.login_author ,name="author-login"),
    path('author/dashboard/', views.author_dashboard,name="author-dashboard"),
    path('author/create_book/', views.create_book,name="create_book"),
    path('author/forgot_password/', views.forgot_password ,name="author-forgot_password"),
    path('author/reset_password/<str:id>/', views.reset_password ,name="author-reset_password"),
    path('author/verification_user/<str:id>/', views.verification_author ,name="author-verification"),
    path('author/view_book/<str:id>/', views.view_book ,name="view_book"),
    path('author/edit_book/<str:id>/', views.edit_book ,name="edit_book"),
    path('author/delete_book/<str:id>/', views.delete_book ,name="delete_book"),
    path('author/download_book/<str:id>/', views.download_book ,name="download_book"),
    path('author/logout/', views.logout_user ,name="logout"),
]