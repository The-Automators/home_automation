from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=55)
    img = models.ImageField(upload_to = 'pics')

class Target:
    id: int
    name: str
    src: str