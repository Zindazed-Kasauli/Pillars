from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# home page view
def index(request):
    #redirects user to login if not logged in
    if not request.user.is_authenticated:
        return redirect('login')

    #redirects user to the home page
    return render(request, "stock/index.html")

# registration page view
def register(request):
    if request.method == 'POST':
        #userCreationForm is a default registration form for creating new user
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #authenticates user
            user = authenticate(username=username, password=password)

            #logins in user
            login(request, user)

            #redirects user to home page
            return redirect('index')
    else:
        #nothing happens
        form = UserCreationForm()
    
    context = {'form':form}
    return render(request, 'registration/register.html', context)

