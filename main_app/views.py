from django.shortcuts import render
from .models import Finch

# Create the home view
def home(request):
    return render(request, 'home.html')

# Create the about view
def about(request):
    return render(request, 'about.html')

# Create the index view
def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', { 'finches': finches })

# Create the detail view
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, 'finches/detail.html', { 'finch': finch })
