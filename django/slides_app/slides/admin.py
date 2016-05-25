from django.contrib import admin

from .models import Current, Slides
# Register your models here.

admin.site.register(Slides)
   
admin.site.register(Current)
