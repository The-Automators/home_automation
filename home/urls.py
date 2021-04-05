from django.urls import path
from home import views # importing views from local dir

# url for home page 
urlpatterns = [
    path('', views.home, name='home'), # main url show when home url is called
    path('menu/<str:id>', views.menu, name='menu'), # submenu url for home page
    path('menu/<str:id>/data', views.data, name='data'), # submenu url for home page
    path('menu/camera/video_feed', views.video_feed, name='video_feed'), # url for camera feed
    path('logout', views.logout, name='logout') # url for logout
]