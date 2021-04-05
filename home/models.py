from django.db import models

# model for menu database
class Menu(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name

# model for menu database
class Room(models.Model):
    name = models.CharField(max_length=55)
    
    def __str__(self):
        return self.name

# referance table for rooms
class Device(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bulb = models.IntegerField(default=-1)
    fan = models.IntegerField(default=-1)
    ac = models.IntegerField(default=-1)
    door = models.IntegerField(default=-1)

    def __str__(self):
        return self.room.name