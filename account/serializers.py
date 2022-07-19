from rest_framework import serializers
from .models import *
from projectfund.models import Project


class AccountLogin(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class ProfileApi(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['birthdate','facebook','country']


class ProjectApi(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
