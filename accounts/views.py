from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  #  Log the user in immediately
            return redirect('home')  #  Redirect to home after login
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


