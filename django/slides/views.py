from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from .models import Current, Slides, Votes
from django.contrib.auth.models import User

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
    current_slide = get_object_or_404(Slides, pk=current.page)
    bad = Votes.objects.filter(slide = current_slide, value = 1).count()
    if(isLecturer=='1'):
        return render(request, 'slides/lecture.html', {'slide':current_slide, 'lecturer':True, 'votes_amplified':bad*5,
                                                       'votes_rest': 100-bad*5})
    else:
        return render(request, 'slides/lecture.html', {'slide':current_slide, 'student':True, 'votes_amplified':bad*5,
                                                       'votes_rest': 100-bad*5})

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
    current_user = User.objects.get(username = get_username())
#    current_slide.votes += 1
#    current_slide.save()
    Votes.objects.filter(user = current_user, slide = current_slide).delete()
    v = Votes(user = current_user, slide = current_slide, value = 1)
    return HttpResponseRedirect(reverse('slides:lecture', args=[0]))

def login(request):
    return render(request, 'slides/login.html') 

def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
	    return render(request, 'slides/index.html')
	else:
	    return HttpResponse('Not active user') 
    else:
	return HttpResponse('user = None')

def home(request):
    return HttpResponseRedirect(reverse('slides:index', args=[request.user.username]))
