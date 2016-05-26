from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from .models import Current, Slides, Votes
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.

@login_required
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
    current_slide = get_object_or_404(Slides, pk=current.page)
    if(isLecturer=='0'):
        try:
            myvote = Votes.objects.get(user = request.user, slide = current_slide)
        except Votes.DoesNotExist:
            v = Votes(user = request.user, slide = current_slide, value = 0)
            v.save()

    good = Votes.objects.filter(slide = current_slide, value = 0).count()
    bad = Votes.objects.filter(slide = current_slide, value = 1).count()
    total = good + bad
    if(isLecturer=='1'):
        if (total == 0):
            total = 1
            good = 1
        return render(request, 'slides/lecture.html', {'slide':current_slide, 'lecturer':True, 'votes_amplified':bad *100 / total, 'votes_rest': good*100/total})
    else:
        return render(request, 'slides/lecture.html', {'slide':current_slide, 'student':True, 'votes_amplified':bad*100/total, 'votes_rest': good*100/ total})

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

def vote_up(request):
    current = get_object_or_404(Current, pk=1)
    '''
    qs = Slides.objects.filter(slide_text=current.slide_name)
    qs = qs.filter(page = current.page)
    slide = qs.reverse()[:1]
    return render(request, 'slides/index.html', {'slide': slide})
    '''
    current_slide = get_object_or_404(Slides, pk=current.page)

    try:
        v = Votes.objects.get(user = request.user, slide = current_slide)
        v.value = 0
        v.save()
    except Votes.DoesNotExist:
        v = Votes(user = request.user, slide = current_slide, value = 0)
        v.save()

    return HttpResponseRedirect(reverse('slides:lecture', args=[0]))

def vote_down(request):
    current = get_object_or_404(Current, pk=1)
    '''
    qs = Slides.objects.filter(slide_text=current.slide_name)
    qs = qs.filter(page = current.page)
    slide = qs.reverse()[:1]
    return render(request, 'slides/index.html', {'slide': slide})
    '''
    current_slide = get_object_or_404(Slides, pk=current.page)
    try:
        v = Votes.objects.get(user = request.user, slide = current_slide)
        v.value = 1
        v.save()
    except Votes.DoesNotExist:
        v = Votes(user = request.user, slide = current_slide, value = 1)
        v.save()
    return HttpResponseRedirect(reverse('slides:lecture', args=[0]))

def home(request):
    return HttpResponseRedirect(reverse('slides:index', args=[request.user.username]))


def logout_view(request):
    print("HERERER")
    
    logout(request)
    return HttpResponseRedirect('/login/')
