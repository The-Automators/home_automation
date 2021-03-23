from django.db import models

# Create your models here.
# model for menu database
class Menu(models.Model):
    name = models.CharField(max_length=55)

# model for submenu database
class SubMenu(models.Model):
    name = models.CharField(max_length=55)
    status = models.BooleanField(default=False)