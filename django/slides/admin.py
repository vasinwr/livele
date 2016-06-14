from django.contrib import admin

from .models import Current, PDF, Votes, Question, Question_Vote, Speed
# Register your models here.

admin.site.register(PDF)
   
admin.site.register(Current)

admin.site.register(Votes)

admin.site.register(Question)

admin.site.register(Question_Vote)

admin.site.register(Speed)
