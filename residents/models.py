from django.db import models
from django.contrib.auth.models import User

class Resident(models.Model):
    username = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    resident_name = models.CharField(max_length=50)
    resident_code = models.CharField(max_length=50, unique=True)
    resident_description = models.CharField(max_length=200)
    resident_contact_person = models.CharField(max_length=80)
    resident_contact_phone = models.CharField(max_length=100)
    resident_contact_email = models.CharField(max_length=100)
    resident_contact_relation = models.CharField(max_length=100)
    
    def __str__(self):
        return self.resident_name  