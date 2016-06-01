import json
from django.db import models
from django.contrib.auth.models import User, Group
from channels import Group as Channel_Group
from django.shortcuts import get_object_or_404
import os

# Create your models here.

class PDF(models.Model):
    filename = models.CharField(max_length=200)
    course = models.ForeignKey(Group, on_delete=models.CASCADE, default = 1)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    current_page = models.IntegerField()

    def __str__(self):
        return self.filename

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

#def rename(instance, filename):
#    ext = filename.split('.')[-1]
#    filename = "current.%s" % (ext)
#    directory = os.path.join('media/uploads', filename)
#    if os.path.isfile(directory):
#        os.remove(directory)
#    return os.path.join('uploads', filename)

#class Pdf(models.Model):
#    pdffile = models.FileField(upload_to=rename)

