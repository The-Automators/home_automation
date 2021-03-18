from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def login(req):
    if req.user.is_authenticated: return redirect('home')
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(req, user)
            return redirect('home')
        messages.info(req, 'Invalid Credentials!!!')
        return redirect('/')
    return render(req, 'login.html')
