from django.contrib import admin

from .models import Current, Slides, Votes, Pdf
# Register your models here.

admin.site.register(Slides)
   
admin.site.register(Current)

admin.site.register(Votes)

admin.site.register(Pdf)
