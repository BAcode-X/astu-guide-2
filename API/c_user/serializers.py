from rest_framework import serializers
from core.models import QuestionPost, AnswerPost


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPost
        fields = ["id", "title", "body", "author", "created_at", "updated_at"]
    
    def create(self, validated_data):
        user = self.context["request"].user
        question = QuestionPost.objects.create(author=user, **validated_data)
        return question
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.save()
        return instance
    
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerPost
        fields = ["id", "body", "author", "question", "created_at", "updated_at"]
        
    def create(self, validated_data):
        user = self.context["request"].user
        answer = AnswerPost.objects.create(author=user, **validated_data)
        return answer
    
    def update(self, instance, validated_data):
        instance.body = validated_data.get("body", instance.body)
        instance.save()
        return instance