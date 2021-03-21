from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/<str:id>', views.menu, name='menu'),
    path('logout', views.logout, name='logout')
]