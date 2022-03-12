from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from ckeditor.fields import RichTextField

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("User must have a username!")
        if not email:
            raise ValueError("User must have an email!")
        if not password:
            raise ValueError("User must have a password!")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        if not username:
            raise ValueError("User must have a username!")
        if not email:
            raise ValueError("User must have an email!")
        if not password:
            raise ValueError("User must have a password!")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    reputation = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    @property
    def name(self):
        return self.first_name + " " + self.last_name


class QuestionPost(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class AnswerPost(models.Model):
    body = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.body[:20]

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name