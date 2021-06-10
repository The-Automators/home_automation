from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
# local dir import
from .models import Menu, Device, Room
from .camera import VideoCapture
from functools import wraps

# decorator for redirect
def redirect_decorator(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated: return redirect('/')
        return function(*args, **kwargs)
    return wrapper

# menu page renderer
@redirect_decorator
def home(request):
    return render(request, 'home.html', {'arrow' : False, 'targets': Menu.objects.all()})

# submenu page renderer
@redirect_decorator
def menu(request, id):
    if id in ['bulb', 'door', 'fan', 'ac']:
        if id == 'bulb':
            row = Device.objects.exclude(bulb = -1)
            data = ["checked" if x.bulb == 1 else "" for x in row]
        elif id == 'door':
            row = Device.objects.exclude(door = -1)
            data = ["checked" if x.door == 1 else "" for x in row]
        elif id == 'fan':
            row = Device.objects.exclude(fan = -1)
            data = ["checked" if x.fan == 1 else "" for x in row]
        elif id == 'ac':
            row = Device.objects.exclude(ac = -1)
            data = ["checked" if x.ac == 1 else "" for x in row]
        room = [x.room for x in row]
        _id = [x.id for x in row]
        return render(request, 'menu.html', {'menu_title' : id, 'arrow' : True, 'data' : zip(room, data, _id)})
    if id in ['camera', 'temperature']:
        return render(request, 'menu2.html', {'menu_title' : id, 'arrow' : True, 'temperature' : 30})
    return redirect('home')

# data feedback from the database and ardiuno
@redirect_decorator
def data(request, id):
    _id = request.GET['id'][1 if request.GET['id'].startswith('c') else 0:]
    status = request.GET['status']
    value = 1 if status == 'true' else 0
    obj = Device.objects.get(id=_id)
    if id == 'bulb':
        obj.bulb = value
        # add Your Code Here for bulb

    elif id == 'door':
        obj.door = value
        # add Your Code Here for door

    elif id == 'fan':
        obj.fan = value
        # add Your Code Here for fan

    elif id == 'ac':
        obj.ac = value
        # add Your Code Here for ac

    obj.save()
    print(id, _id, status, obj.bulb, obj.door, obj.fan, obj.ac)
    return redirect(f'/home/menu/{id}')

# generating camera frame
def gen(cam):
    while True:
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
                + cam.get_frame() + b'\r\n\r\n')

# sending camera feed back
def video_feed(request):
    return StreamingHttpResponse(gen(VideoCapture(0)),
                content_type='multipart/x-mixed-replace; boundary=frame')

# user logout
def logout(request):
    auth.logout(request)
    return redirect('/')
