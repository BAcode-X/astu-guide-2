from django.shortcuts import render
from django.views.generic import ListView, DetailView
from rest_framework import exceptions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from core.models import User, BlogPost
from .authentication import JWTAuthentication

# Create your views here.


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data.get("password") != data.get("password_confirm"):
            raise exceptions.APIException("Passwords do not match")

        data["is_admin"] = "api/admin" in request.path

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username).first()

        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Incorrect password")

        scope = "user" if "api/user" in request.path else "admin"

        if user.is_admin and scope == "user":
            raise exceptions.AuthenticationFailed("Unauthorized!")

        token = JWTAuthentication.generate_jwt(user.id, scope=scope)

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"message": "success"}
        return response


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        data["is_admin"] = user.is_admin

        return Response(data)


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie(key="jwt")
        response.data = {"message": "success"}
        return response


class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        data = request.data

        if data.get("password") != data.get("password_confirm"):
            raise exceptions.APIException("Passwords do not match")

        user.set_password(data["password"])
        user.save()
        return Response(UserSerializer(user).data)

def home(request):
    return render(request, "common/index.html", {})

class NewsListView(ListView):
    model = BlogPost
    template_name = "common/news.html"
    context_object_name = "posts"

class NewsDetailView(DetailView):
    model = BlogPost
    template_name = "common/news_detail.html"