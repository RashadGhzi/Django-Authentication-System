from django.db import models
from time import strftime

# Create your models here
class mood(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateField()
    def __str__(self) -> str:
        return self.date.strftime("%m/%d/%Y") + f" {self.name} {self.email}"