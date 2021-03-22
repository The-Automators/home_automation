from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http.response import StreamingHttpResponse
from home.camera import VideoCapture
from home.models import Menu, SubMenu

# Create your views here.
def home(req):
    if not req.user.is_authenticated: return redirect('/')
    data = Menu.objects.all()
    return render(req, 'home.html', {'arrow' : False, 'targets': data})

def gen(cam):
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

def menu(req, id):
    if not req.user.is_authenticated: return redirect('/')
    if id in ['bulb', 'door', 'fan', 'ac']:
        data = SubMenu.objects.all()
        return render(req, 'menu.html', {'menu_title' : id, 'arrow' : True, 'targets' : data,})
    if id in ['camera', 'temperature']:
        return render(req, 'menu2.html', {'menu_title' : id, 'arrow' : True, 'temperature' : 30})
    return redirect('home')

def video_feed(req):
    return StreamingHttpResponse(gen(VideoCapture()),
        content_type='multipart/x-mixed-replace; boundary=frame')

def logout(req):
    auth.logout(req)
    return redirect('/')