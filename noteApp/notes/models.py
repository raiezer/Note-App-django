from django.db import models

# Create your models here.
class User_model(models.Model):
    username=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=20)


class Note_model(models.Model):
    date_time=models.DateTimeField()
    notes=models.CharField(max_length=20)
    user_id = models.IntegerField()

    def __str__(self):
        return self.user_id
