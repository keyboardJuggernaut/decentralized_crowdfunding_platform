from djongo import models

class Event(models.Model):
    _id = models.ObjectIdField()
    type = models.CharField(max_length=50)
    times = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
