from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import Menu, Target

# Create your views here.
def home(req):
    if not req.user.is_authenticated: return redirect('/')
    t = [Target() for i in range(6)]
    t[0].name, t[0].src = ['camera']*2
    t[1].name, t[1].src = ['temperature']*2 
    t[2].name, t[2].src = ['ac', 'ac1']
    t[3].name, t[3].src = ['bulb', 'bulb1']
    t[4].name, t[4].src = ['door', 'door1']
    t[5].name, t[5].src = ['fan', 'fan1']
    return render(req, 'home.html', {'arrow' : False, 'targets': t})

def menu(req, id):
    if not req.user.is_authenticated: return redirect('/')
    if id in ['bulb', 'door', 'fan', 'ac']:
        t = [Target() for i in range(6)]
        for i in t: i.src = id
        t[0].name = 'bed room 1'.capitalize()
        t[1].name = 'bed room 2'.capitalize()
        t[2].name = 'kitchen'.capitalize()
        t[3].name = 'hall room'.capitalize()
        t[4].name = 'drawing room'.capitalize()
        t[5].name = 'dining area'.capitalize()
        return render(req, 'menu.html', {'menu_title' : id.title(), 'arrow' : True, 'targets' : t})
    if id in ['camera', 'temperature']:
        return render(req, 'menu2.html', {'menu_title' : id.title(), 'arrow' : True, 'temperature' : 30})
    return redirect('home')

def logout(req):
    auth.logout(req)
    return redirect('/')