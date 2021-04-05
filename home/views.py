from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
# local dir import
from .models import Menu, Device, Room
from .camera import VideoCapture 

# menu page renderer
home = lambda req: redirect('/') if not req.user.is_authenticated else render(req, 'home.html', 
                {'arrow' : False, 'targets': Menu.objects.all()})

# submenu page renderer
def menu(req, id):
    if not req.user.is_authenticated: return redirect('/')
    if id in ['bulb', 'door', 'fan', 'ac']:
        if id == 'bulb': 
            row = Device.objects.exclude(bulb = -1)
            data = ["true" if x.bulb == 1 else "false" for x in row]
        elif id == 'door': 
            row = Device.objects.exclude(door = -1)
            data = ["true" if x.bulb == 1 else "false" for x in row]
        elif id == 'fan': 
            row = Device.objects.exclude(fan = -1)
            data = ["true" if x.bulb == 1 else "false" for x in row]
        elif id == 'ac': 
            row = Device.objects.exclude(ac = -1)
            data = ["true" if x.bulb == 1 else "false" for x in row]
        room = [x.room for x in row]
        return render(req, 'menu.html', {'menu_title' : id, 'arrow' : True, 'data' : zip(room, data)})
    if id in ['camera', 'temperature']:
        return render(req, 'menu2.html', {'menu_title' : id, 'arrow' : True, 'temperature' : 30})
    return redirect('home')

def data(req, id):
    print(id, req.GET['id'], req.GET['status'])
    return redirect(f'/home/menu/{id}')

# generating camera frame 
def gen(cam):
    while True: yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + cam.get_frame() + b'\r\n\r\n')

# sending camera feed back
video_feed = lambda req: StreamingHttpResponse(gen(VideoCapture()), content_type='multipart/x-mixed-replace; boundary=frame')

# user logout 
def logout(req):
    auth.logout(req)
    return redirect('/')
