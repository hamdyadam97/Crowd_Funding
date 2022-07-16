from django import forms
from django.contrib.auth.models import User
import re
from .models import Account, Profile


class AccountCreate(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    mobile_phone = forms.CharField(max_length=11, help_text="phone must be start with 010,011,012,015")
    # email = forms.EmailField(help_text="email must uniqe")

    class Meta:
        model = Account
        fields = ['firstname', 'lastname', 'email', 'password', 'confirm_password', 'mobile_phone', 'image']

    def clean_confirm_password(self):
        cd = self.cleaned_data
        print(cd)
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError(' password not correct ')
        return cd['confirm_password']

    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError("there are eamil already exists")
        return cd['email']

    def clean_mobile_phone(self):
        cd = self.cleaned_data
        reg = '^01[0125][0-9]{8}$'
        if re.match(reg, cd['mobile_phone']) is None:
            raise forms.ValidationError("phone must be in egypt")
        return cd['mobile_phone']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['firstname', 'lastname','mobile_phone', 'image']

    def clean_mobile_phone(self):
        cd = self.cleaned_data
        reg = '^01[0125][0-9]{8}$'
        if re.match(reg, cd['mobile_phone']) is None:
            raise forms.ValidationError("phone must be in egypt")
        return cd['mobile_phone']


class CreateProfile(forms.ModelForm):
    birthdate = forms.CharField(widget=forms.SelectDateWidget,)
    class Meta:
        model = Profile
        fields = ['birthdate', 'facebook', 'country']
