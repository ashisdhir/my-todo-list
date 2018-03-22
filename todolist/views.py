from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, forms
from .models import todo
from django.contrib.auth.decorators import login_required
from .forms import todoNewForm
from django.utils import timezone


# Create your views here.
def index(request):
    return render(request, 'todolist/index.html')


def todo_new(request):
    if request.method == 'POST':
        form = todoNewForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.name = request.user
            todo.created = timezone.now()
            todo.save()
            return redirect('details')
    else:
        form = todoNewForm()

    return render(request, 'todolist/todo_edit.html', {'form': form})


@login_required()
def details(request):
    items = todo.objects.filter(name=request.user).order_by('created')[:10]

    return render(request, 'todolist/details.html', {'items': items})


def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = forms.UserCreationForm()
    return render(request, 'todolist/signup.html', {'form':form})