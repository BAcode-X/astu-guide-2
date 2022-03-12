from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("news/", views.NewsListView.as_view(), name="news"),
    path("news/<int:pk>", views.NewsDetailView.as_view(), name="news_detail"),
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("login", views.LoginAPIView.as_view(), name="login"), #
    path("user/", views.UserAPIView.as_view(), name="user"), #
    path("logout/", views.LogoutAPIView.as_view(), name="logout"), #
    path("account/info/", views.ProfileInfoAPIView.as_view(), name="profile"), #
    path("account/password/", views.ProfilePasswordAPIView.as_view(), name="change_password"), #
]
