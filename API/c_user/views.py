from statistics import mode
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions, serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import QuestionPost, AnswerPost, Location
from .serializers import QuestionSerializer, AnswerSerializer
import os
from dotenv import load_dotenv


load_dotenv()

# Create your views here.

class AskQuestionAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = QuestionSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AnswerAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = AnswerSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class QuestionAPIView(APIView):
    def get(self, request):
        questions = QuestionPost.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


def questions_list(request):
    questions = QuestionPost.objects.all()
    return render(request, "c_user/questions_list.html", {"questions": questions})

def ask_question(request):
    return render(request, "c_user/ask_question.html", {})

def show_path(request):
    map_box_token = os.getenv("MAP_BOX_TOKEN")
    return render(request, "c_user/shortest_path.html", {'map_box_token': map_box_token})

def find_location(request):
    all_locations = Location.objects.all()
    if request.method == "GET":
        return render(request, "c_user/find_location.html", {'all_locations': all_locations})
    elif request.method == "POST":
        map_box_token = os.getenv("MAP_BOX_TOKEN")
        origin = request.POST.get("location")
        o_instance = Location.objects.get(name=origin)
        destination = request.POST.get("destination")
        d_instance = Location.objects.get(name=destination)
        mental = False
        if destination == origin:
            clinic = Location.objects.get(name="ASTU Clinic")
            mental = True
            return render(request, "c_user/shortest_path.html", {'all_locations': all_locations, 'location': o_instance, 'destination': clinic, 'mental': mental, 'map_box_token': map_box_token})
        return render(request, "c_user/shortest_path.html", {'location': o_instance, 'destination': d_instance, 'map_box_token': map_box_token, 'mental': mental})

class QuestionDetailView(DetailView):
    model = QuestionPost
    template_name = "c_user/question_detail.html"


class AskQuestion(LoginRequiredMixin,CreateView):
    model = QuestionPost
    template_name = "c_user/ask_question.html"