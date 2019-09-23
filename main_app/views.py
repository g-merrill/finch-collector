from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Finch, Toy, Photo
from .forms import FeedingForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'finchcollector-gam'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, 'finches/index.html', { 'finches': finches })

@login_required
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch,
        'feeding_form': feeding_form,
        'toys': toys_finch_doesnt_have
    })

class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = ['name', 'species', 'description', 'age']
    template_name = 'finches/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['species', 'description', 'age']
    template_name = 'finches/form.html'

class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches/'
    template_name = 'finches/confirm_delete.html'

@login_required
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

@login_required
def add_photo(request, finch_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, finch_id=finch_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', finch_id=finch_id)

@login_required
def delete_photo(request, finch_id, photo_id):
    Photo.objects.get(id=photo_id).delete()
    return redirect('detail', finch_id=finch_id)

@login_required
def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

@login_required
def unassoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id=finch_id)

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/form.html'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    context_object_name = 'toys'
    template_name = 'toys/index.html'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/show.html'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['color']
    template_name = 'toys/form.html'

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'
    template_name = 'toys/confirm_delete.html'