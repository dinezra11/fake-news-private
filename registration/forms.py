from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    firstname = forms.CharField()
    lastname = forms.CharField()
    isexpert = forms.BooleanField(required=False)
    pic = forms.ImageField(required=False)
    isAdmin = forms.BooleanField(required=False)
    Certificate = forms.ImageField(required=False)
    Pending = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'firstname', 'email', 'lastname', 'password1', 'password2', 'isexpert', 'pic',
                  'isAdmin', 'Certificate', 'Pending']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean_firstname(self):
        firstname = self.cleaned_data.get('firstname')
        for char in firstname:
            if char.isdigit():
                raise forms.ValidationError("A first name cannot contain digits")
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        for char in lastname:
            if char.isdigit():
                raise forms.ValidationError("A last name cannot contain digits")
        return lastname

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        # if password1 != password2:
        #   raise forms.ValidationError("Your passwords do not match")
        return password1
