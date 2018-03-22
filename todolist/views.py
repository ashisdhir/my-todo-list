from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, forms
from .models import todo
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'todolist/index.html')

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