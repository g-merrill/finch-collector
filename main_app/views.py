from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Toy
from .forms import FeedingForm

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
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch, 'feeding_form': feeding_form
    })

class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['species', 'description', 'age']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'

def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyIndex(ListView):
    model = Toy
    context_object_name = 'toys'
    template_name = 'toys/index.html'