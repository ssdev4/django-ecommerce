from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from checkout.models import Order

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # import pdb; pdb.set_trace()
            session_key = request.session.session_key
            user = form.save()
            login(request, user)  # Automatically log in user after signup
            # Transfer any guest orders to the new user
            if session_key:
                Order.objects.filter(user__isnull=True, session_key=session_key).update(user=user)

            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})
