from django.db import models
from django.contrib.auth.models import User


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

class Pdf(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
