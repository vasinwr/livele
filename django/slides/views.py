from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Current, Slides

# Create your views here.

def index(request):
    return render(request, 'slides/index.html') 

def lecturer(request):
    return HttpResponseRedirect(reverse('slides:lecture', args=[1]))

def student(request):
    return HttpResponseRedirect(reverse('slides:lecture', args=[0]))

def lecture(request, isLecturer):
    current = get_object_or_404(Current, pk=1)
    '''
    qs = Slides.objects.filter(slide_text=current.slide_name)
    qs = qs.filter(page = current.page)
    slide = qs.reverse()[:1]
    return render(request, 'slides/index.html', {'slide': slide})
    '''
    slide = get_object_or_404(Slides, pk=current.page)
    if(isLecturer=='1'):
        return render(request, 'slides/lecture.html', {'slide':slide, 'lecturer':True, 'votes_amplified':slide.votes*5,
                                                       'votes_rest': 100-slide.votes*5})
    else:
        return render(request, 'slides/lecture.html', {'slide':slide, 'student':True, 'votes_amplified':slide.votes*5,
                                                       'votes_rest': 100-slide.votes*5})

def next_page(request):
    current = get_object_or_404(Current, pk=1)
    try:
	slide = Slides.objects.get(page = current.page + 1)
	current.page += 1
	current.save()
    except Slides.DoesNotExist:
	pass
    return HttpResponseRedirect(reverse('slides:lecture', args=[1]))

def prev_page(request):
    current = get_object_or_404(Current, pk=1)
    try:
	slide = Slides.objects.get(page = current.page - 1)
	current.page -= 1
	current.save()
    except Slides.DoesNotExist:
	pass
    return HttpResponseRedirect(reverse('slides:lecture', args=[1]))

def vote_current(request):
    current = get_object_or_404(Current, pk=1)
    '''
    qs = Slides.objects.filter(slide_text=current.slide_name)
    qs = qs.filter(page = current.page)
    slide = qs.reverse()[:1]
    return render(request, 'slides/index.html', {'slide': slide})
    '''
    current_slide = get_object_or_404(Slides, pk=current.page)
    current_slide.votes += 1
    current_slide.save()
    return HttpResponseRedirect(reverse('slides:lecture', args=[0]))
