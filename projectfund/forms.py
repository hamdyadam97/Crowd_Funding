from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
import re
from .models import Project,ProjectImage,ProjectTag,Rate,Comment


class FormDonate(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['donations']


    def clean_total_target(self):
        cd = self.cleaned_data
        reg = '[1-9]'
        if re.match(reg, cd['total_target']) is None:
            raise forms.ValidationError("not valid")
        return cd['total_target']


class CreateProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'end_date']


class ImageProjectFrom(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']


class ProjectTagForm(forms.ModelForm):
    class Meta:
        model = ProjectTag
        fields = ['tag']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class form_rate(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('rating',)
