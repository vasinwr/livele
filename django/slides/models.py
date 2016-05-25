from django.db import models

# Create your models here.

class Current(models.Model):
    slide_name = models.CharField(max_length=200)
    page = models.IntegerField()


class Slides(models.Model):
    slide_text = models.CharField(max_length=200)
    page = models.IntegerField()
    img_source = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.slide_text +' '+ str(self.page)
