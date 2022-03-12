from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('common.urls')),
    path("find-path/", views.find_location, name="find_path"),
    path('questions-list/', views.questions_list, name='question_list'),
    path('ask-question/', views.ask_question, name='ask_question'),
]