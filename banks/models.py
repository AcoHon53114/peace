from django.db import models
from datetime import datetime
# Create your models here.
from residents.models import Resident
from banks.choices import payment_method_choices


class Bank(models.Model):
    resident_id = models.ForeignKey(Resident, on_delete=models.DO_NOTHING, related_name='banks_by_resident_id')
    resident_name = models.ForeignKey(Resident, on_delete=models.DO_NOTHING, related_name='banks_by_resident_name')
    payment_method = models.CharField(max_length=20,choices=payment_method_choices.items())
    depositslip_photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    message = models.TextField(max_length=50)
    uploaded_date = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.resident_name