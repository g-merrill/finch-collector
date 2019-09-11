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
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch,
        'feeding_form': feeding_form,
        'toys': toys_finch_doesnt_have
    })

class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'
    template_name = 'finches/form.html'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['species', 'description', 'age']
    template_name = 'finches/form.html'

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'
    template_name = 'finches/confirm_delete.html'

def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

def unassoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id=finch_id)

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/form.html'

class ToyList(ListView):
    model = Toy
    context_object_name = 'toys'
    template_name = 'toys/index.html'

class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/show.html'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['color']
    template_name = 'toys/form.html'

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
    template_name = 'toys/confirm_delete.html'