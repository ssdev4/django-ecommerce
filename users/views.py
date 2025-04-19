from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in user after signup
            return redirect('/')  # or wherever you want to redirect
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})
