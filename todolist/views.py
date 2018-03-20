from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, forms

# Create your views here.
def index(request):
    return render(request, 'todolist/index.html')

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