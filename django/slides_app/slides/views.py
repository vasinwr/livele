from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Current, Slides

# Create your views here.

def index(request):
    
    current = get_object_or_404(Current, pk=1)
    '''
    qs = Slides.objects.filter(slide_text=current.slide_name)
    qs = qs.filter(page = current.page)
    slide = qs.reverse()[:1]
    return render(request, 'slides/index.html', {'slide': slide})
    '''
    slide = get_object_or_404(Slides, pk=current.page)
    return render(request, 'slides/index.html', {'slide':slide})
'''
def index(request):
    return HttpResponse("Hello, you are at the slides index.")
'''

def next_page(request):
    current = get_object_or_404(Current, pk=1)
    current.page += 1
    current.save()
    return HttpResponseRedirect(reverse('slides:index'))

def prev_page(request):
    current = get_object_or_404(Current, pk=1)
    current.page -= 1
    current.save()
    return HttpResponseRedirect(reverse('slides:index'))
