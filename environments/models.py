from django.db import models
from datetime import datetime
# Create your models here.

class Voice(models.Model):
    name = models.TextField(max_length=30)
    photo= models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(max_length=50)
    is_published = models.BooleanField(default=True)
    
    def _str_(self):
        return self.name
    
    
    
    

