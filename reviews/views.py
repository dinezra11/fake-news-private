from django.shortcuts import render
from .models import Review


# Create your views here.
def viewForm(request):
    if request.method == 'POST':
        data = request.POST # Dictionary of the input data
        Review.objects.create(
            name = data['name'],
            email = data['email'],
            title = data['title'],
            content = data['description']
        )

        return render(request, 'reviews/submitted.html', None)
    else:
        return render(request, 'reviews/reviews.html', None)
