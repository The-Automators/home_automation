from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from home.camera import VideoCapture
from home.models import Menu, SubMenu

# Create your views here.
home = lambda req: redirect('/') if not req.user.is_authenticated else render(req, 'home.html', {'arrow' : False, 'targets': Menu.objects.all()})

def gen(cam):
    while True: yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + cam.get_frame() + b'\r\n\r\n')

video_feed = lambda req: StreamingHttpResponse(gen(VideoCapture()), content_type='multipart/x-mixed-replace; boundary=frame')

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