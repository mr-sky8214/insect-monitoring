
# forms.py
from django import forms
from .models import *
import datetime 
import pytz 
  
class InsectImageForm(forms.ModelForm):
    # def clean_name(self):
    #     date = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')))
    #     date = date.split(' ')
    #     date[1] = date[1].split('.')
        
    #     self.name = str(date[0]) + "-" + str(date[1][0].replace(':', '-')) 
    #     return self.name
  
    class Meta:
        model = Insect_Images
        fields =['insect_input_img']