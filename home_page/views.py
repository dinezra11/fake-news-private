from django.shortcuts import render
from registration.models import UserData
from articles.models import PredictionApproves
from django.contrib.auth.models import User
import os
from django.conf import settings


def home(request):
    return render(request, 'home.html')

def myarticle(request):

    articles = PredictionApproves.objects.filter(expertId=request.user.id)
    return render(request, 'myarticle.html' ,{'articles': articles})



def myProfile(request):
    if request.method == 'POST':
        if request.POST.get('useridd'):
            idd=request.POST.get('useridd')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            profilepicture = request.FILES.get('profilepicture')
            certificatepicture = request.POST.get('certificatepicture')
            if first_name:
                UserData.objects.filter(user_id=idd).update(firstname=first_name)
            if last_name:
                UserData.objects.filter(user_id=idd).update(lastname=last_name)
            if password1 and password2 and password1 == password2:
                user = User.objects.get(username=idd)
                user.set_password(password1)
                user.save()
            if profilepicture:
                user1 = UserData.objects.get(user_id=idd)
                user1.pic = profilepicture
                user1.save()
            if certificatepicture:
                user2 = UserData.objects.get(user_id=idd)
                user2.Certificate = certificatepicture
                user2.save()

            users = UserData.objects.filter(user_id=idd)
            return render(request, 'myProfile.html', {'users': users})


        else:
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            profilepicture = request.FILES.get('profilepicture')
            certificatepicture = request.POST.get('certificatepicture')
            if first_name:
                UserData.objects.filter(user_id=request.user.id).update(firstname=first_name)
            if last_name:
                UserData.objects.filter(user_id=request.user.id).update(lastname=last_name)
            if password1 and password2 and password1 == password2:
                user = User.objects.get(username=request.user.id)
                user.set_password(password1)
                user.save()
            if profilepicture:
                user1 = UserData.objects.get(user_id=request.user.id)
                user1.pic = profilepicture
                user1.save()
            if certificatepicture:
                user2 = UserData.objects.get(user_id=request.user.id)
                user2.Certificate = certificatepicture
                user2.save()

    users = UserData.objects.filter(user_id=request.user.id)
    return render(request, 'myProfile.html', {'users': users})
