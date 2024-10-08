from django.db import models
from datetime import datetime

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=80)
    comment = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.name