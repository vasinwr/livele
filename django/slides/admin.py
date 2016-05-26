from django.contrib import admin

from .models import Current, Slides, Votes
# Register your models here.

admin.site.register(Slides)
   
admin.site.register(Current)

admin.site.register(Votes)
