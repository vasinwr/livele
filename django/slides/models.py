import json
from django.db import models
from django.contrib.auth.models import User, Group
from channels import Group as Channel_Group
from django.shortcuts import get_object_or_404
import os
from django.forms import ModelForm

import binascii

# Create your models here.

class Token(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super(Token, self).save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.token


###############

def rename(instance, filename):
    return '/'.join([filename])

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
        except: pass           
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
        return str(self.owner) +' '+ str(self.pdf) +' page'+ str(self.page)  + (' active' if (self.active == 1) else ' inactive')

class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE)
    page = models.IntegerField()
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) +' '+ str(self.pdf) +' page'+ str(self.page)  + (' happy' if (self.value == 0) else ' unhappy')

    def send_notif():
        notification = {
            "green_bar": 100,
            "red_bar": 0,
        }
        Channel_Group("all").send({
            "text": json.dumps(notification),
        })


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


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE)
    page = models.IntegerField()
    text = models.TextField(verbose_name = 'Question')

    def __str__(self):
        return str(self.user) +' '+ str(self.pdf) +' page'+ str(self.page)+' '  + self.text

class Question_Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) +' likes '+ str(self.question)

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text']
