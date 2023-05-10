from django.shortcuts import render, redirect
from registration.models import UserData
from django.contrib.auth.models import User


def users(request):
    onlineuser = UserData.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        if request.POST.get('radio') == 'expert':
            users = UserData.objects.filter(isexpert=True)
            return render(request, 'users.html', {'users': users, 'onlineuser': onlineuser})
        if request.POST.get('radio') == 'normal':
            users = UserData.objects.filter(isexpert=False,isAdmin=False)
            return render(request, 'users.html', {'users': users, 'onlineuser': onlineuser})
        if request.POST.get('radio') == 'all':
            users = UserData.objects.all()
            return render(request, 'users.html', {'users': users, 'onlineuser': onlineuser})

    users = UserData.objects.all()
    return render(request, 'users.html', {'users': users, 'onlineuser': onlineuser})


def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('users')


def approve(request, id):
    UserData.objects.filter(user_id=id).update(Pending=False)
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect('users')
