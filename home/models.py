from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=55)

class SubMenu(models.Model):
    name = models.CharField(max_length=55)
    status = models.BooleanField(default=False)

class Target:
    id: int
    name: str
    src: str