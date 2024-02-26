from django.db import models

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date_time = models.DateTimeField()

    def __str__(self):
        return self.name
