from django.db import models
from datetime import datetime
from residents.models import Resident
from banks.choices import payment_method_choices, payment_month_choices, payment_year_choices

def current_year():
    return str(datetime.now().year)

def current_month():
    month_number = datetime.now().month
    for key, value in payment_month_choices.items():
        if value.startswith(str(month_number)):
            return key
    return ''

class Bank(models.Model):
    resident_id = models.IntegerField()
    resident_name = models.CharField(max_length=200)
    resident_code = models.CharField(max_length=200) 
    payment_method = models.CharField(max_length=20, choices=payment_method_choices.items())
    payment_month = models.CharField(max_length=20, choices=payment_month_choices.items(), default=current_month)
    payment_year = models.CharField(max_length=20, choices=payment_year_choices.items(), default=current_year)
    depositslip_photo = models.FileField(upload_to='photos/%Y/%m/%d/')
    message = models.TextField(max_length=50)
    uploaded_date = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return str(self.resident_name)