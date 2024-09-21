from django.db import models
from datetime import datetime
from environments.choices import title_choices


# Create your models here.
class Booking(models.Model):
    title = models.CharField(max_length=20,choices=title_choices.items(),default='預約參觀選位')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    visit_date_time = models.DateTimeField(default=datetime.now, blank=True)
    comment = models.TextField(blank=True)
    submit_date = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.title
    
    
    
    

