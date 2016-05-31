import json
from django.db import models
from django.contrib.auth.models import User
from channels import Group
from django.shortcuts import get_object_or_404
import os

# Create your models here.

class Current(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    slide_name = models.CharField(max_length=200)
    page = models.IntegerField()
    active = models.IntegerField(default = 0)


class Slides(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    slide_text = models.CharField(max_length=200)
    page = models.IntegerField()
    img_source = models.CharField(max_length=200)

    def __str__(self):
        return self.slide_text +' '+ str(self.page)

class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slide = models.ForeignKey(Slides, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def send_notification(self, votes):
        good = votes['good'] * 100 / votes['total']
        bad = votes['bad'] * 100 / votes['total']
        notification = {
            "green_bar": good,
            "red_bar": bad,
        }
        Group("all").send({
            "text": json.dumps(notification),
        })

def rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "current.%s" % (ext)
    directory = os.path.join('media/uploads', filename)
    if os.path.isfile(directory):
        os.remove(directory)
    return os.path.join('uploads', filename)

class Pdf(models.Model):
    docfile = models.FileField(upload_to=rename)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Pdf.objects.get(id=self.id)
            if this.image != self.docfile:
                this.docfile.delete(save=False)
        except: pass # when new photo then we do nothing, normal case          
        super(Pdf, self).save(*args, **kwargs)
 
