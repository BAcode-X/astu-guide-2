from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('common.urls')),
    path('create_post/', views.BlogPostCreateView.as_view(), name='create_post'), 
]