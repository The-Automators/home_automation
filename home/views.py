from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from home.models import Menu, Target, SubMenu

# Create your views here.
def home(req):
    if not req.user.is_authenticated: return redirect('/')
    data = Menu.objects.all()
    return render(req, 'home.html', {'arrow' : False, 'targets': data})

def menu(req, id):
    if not req.user.is_authenticated: return redirect('/')
    if id in ['bulb', 'door', 'fan', 'ac']:
        data = SubMenu.objects.all()
        return render(req, 'menu.html', {'menu_title' : id, 'arrow' : True, 'targets' : data,})
    if id in ['camera', 'temperature']:
        return render(req, 'menu2.html', {'menu_title' : id, 'arrow' : True, 'temperature' : 30})
    return redirect('home')

def logout(req):
    auth.logout(req)
    return redirect('/')