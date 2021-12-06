from django.db import models
from django.contrib import admin
import datetime 
import pytz 

# Create your models here.
class Insect_Images(models.Model):
    id = models.AutoField(primary_key = True)
    date = models.DateTimeField(blank = True, default=datetime.datetime.now)
    insect_input_img = models.ImageField(upload_to='input_images/')
    insect_detected_img = models.ImageField(blank=True,upload_to='detected_images/',default = None)
    counts = models.TextField(blank=True, default="") 

    def __str__(self):
        date = str(self.date)
        date = date.split(' ')
        date[1] = date[1].split('.')
        self.name = str(date[0]) + "-" + str(date[1][0].replace(':', '-')) 
        return "Insect_Img_" + str(self.id) + "_" + str(date[0]) + "-" + str(date[1][0].replace(':', '-'))
admin.site.register(Insect_Images)