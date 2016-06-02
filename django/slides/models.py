import json
from django.db import models
from django.contrib.auth.models import User, Group
from channels import Group as Channel_Group
from django.shortcuts import get_object_or_404
import os
from django.forms import ModelForm

# Create your models here.

def rename(instance, filename):
    return '/'.join([instance.course.name, filename])

class PDF(models.Model):
    filename = models.CharField(max_length=200)
    course = models.ForeignKey(Group, on_delete=models.CASCADE, default = 1)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    current_page = models.IntegerField(default = 1)
    pdffile = models.FileField(upload_to=rename)

    def __str__(self):
        return self.filename

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = PDF.objects.get(id=self.id)
            if this.pdffile != self.pdffile:
                this.pdffile.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(PDF, self).save(*args, **kwargs)

class PDFForm(ModelForm):
    class Meta:
        model = PDF
        fields = ['pdffile', 'filename']

class Current(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE, default = 1) 
    page = models.IntegerField()
    active = models.IntegerField(default = 0)

    def __str__(self):
        return self.owner +' '+ str(self.pdf) +' '+ str(self.page)  + ('active' if (self.active == 1) else 'inactive')

class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE)
    page = models.IntegerField()
    value = models.IntegerField(default=0)

    def send_notification(self, votes):
        good = votes['good'] * 100 / votes['total']
        bad = votes['bad'] * 100 / votes['total']
        notification = {
            "green_bar": good,
            "red_bar": bad,
        }
        Channel_Group("all").send({
            "text": json.dumps(notification),
        })


#class PdfModel(models.Model):
#    pdffile = models.FileField(upload_to=rename)

