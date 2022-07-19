from rest_framework import serializers
from .models import Project,ProjectImage,ProjectTag,Rate,Comment


class ApiProjectAll(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectImageApi(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'


class ProjectTagApi(serializers.ModelSerializer):
    class Meta:
        model = ProjectTag
        fields = '__all__'

class CommentApi(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class RateApi(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'
