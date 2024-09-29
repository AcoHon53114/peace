from django.db import models
from django.utils import timezone
from informations.choices import title_choices
from datetime import datetime


# Create your models here.
class Booking(models.Model):
    title = models.CharField(max_length=20,choices=title_choices.items(),default='預約參觀選位')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    visit_date_time = models.DateTimeField(default=datetime.now, blank=True)
    comment = models.TextField(blank=True, null=True)
    submit_date = models.DateTimeField(default=datetime.now, blank=True)
    visit_date = models.DateField(default=timezone.now)  # 新增的日期欄位
    visit_time = models.TimeField(default=timezone.now) 
    
    def __str__(self):
        return f"{self.name} - {self.visit_date} {self.visit_time}"