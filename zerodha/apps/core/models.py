from django.db import models

# Create your models here.

class Bava(models.Model):
    SC_CODE = models.CharField(max_length=255)
    SC_NAME = models.CharField(max_length=255)
    OPEN = models.CharField(max_length=255)
    HIGH = models.CharField(max_length=255)
    LOW = models.CharField(max_length=255)
    CLOSE = models.CharField(max_length=255)

def __str__(self):
        return self.SC_NAME