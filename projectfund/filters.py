import django_filters

from .models import Project,ProjectTag


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ['title']


class ProjectFilterTag(django_filters.FilterSet):
    class Meta:
        model = ProjectTag
        fields = ['tag']
    