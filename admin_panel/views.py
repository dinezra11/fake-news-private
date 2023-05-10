from django.shortcuts import render
from registration.models import UserData
from registration.models import User


# Create your views here.
def approve_list(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')

        if request.POST.get('button') == 'Deny':
            # Delete User
            User.objects.filter(id=userId).delete()
        else:
            # Approve User
            UserData.objects.filter(id=userId).update(Pending=False)
            User.objects.filter(id=userId).update(is_active=True)

    users = UserData.objects.filter(Pending=True)

    return render(request, 'admin_panel/approvelist.html', {'users': users})
