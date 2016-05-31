from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from .models import Current, Slides, Votes, Pdf 
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import PdfForm


# Create your views here.

@login_required
def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Pdf(pdffile=request.FILES['pdffile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('slides:index'))
    else:
        form = PdfForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Pdf.objects.all()
    '''
    return render_to_response(
        'slides/index.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
    '''
    # Render list page with the documents and the form
    if(request.user.groups.filter(name = 'Lecturer').count() == 1):
        return render(request, 'slides/index.html', {'lecturer':True, 'lectureList': Slides.objects.values_list('slide_text', flat=True).distinct(), 'documents': documents, 'form': form})
    else:
        return render(request, 'slides/index.html', {'lectureList': Slides.objects.values_list('slide_text', flat=True).distinct(), 'documents': documents, 'form': form})

@login_required
def select(request, name):
#deactive all other actives.
    try:
        other = Current.objects.get(owner = request.user, active=1)
        other.active = 0
        other.save()
    except Current.DoesNotExist:
        pass

    try:
        current = Current.objects.get(owner = request.user, slide_name = name)
        current.active = 1
        current.save()
    except Current.DoesNotExist:
        current = Current(owner = request.user, slide_name = name, page=1, active=1)
        current.save()

    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def upload(request):
# create lecturer's current at page 1 immediately after upload.
    pass

@login_required
def lecture(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
    try:
        current_slide = Slides.objects.get(slide_text = current.slide_name, page= current.page)
    except Slides.DoesNotExist:
        return HttpResponseNotFound()

    votes = get_votes(request);
    good = votes['good']
    bad = votes['bad']
    total = votes['total']
    if(request.user.groups.filter(name = 'Lecturer').count() == 1):
        return render(request, 'slides/lecture.html', {'slide':current_slide, 'lecturer':True, 'votes_amplified':bad *100 / total, 'votes_rest': good*100/total})
    else:
        return render(request, 'slides/lecture.html', {'slide':current_slide, 'student':True, 'votes_amplified':bad*100/total, 'votes_rest': good*100/ total})

def get_votes(request):
    current = get_object_or_404(Current, owner = request.user, active=1)

    try:
        current_slide = Slides.objects.get(slide_text = current.slide_name, page= current.page)
    except Slides.DoesNotExist:
        return HttpResponseNotFound()

    canVote = Current.objects.get(owner = current_slide.lecturer, slide_name = current_slide.slide_text).page >= current.page
    if(canVote and request.user.groups.filter(name = 'Student').count() == 1):
        try:
            myvote = Votes.objects.get(user = request.user, slide = current_slide)
        except Votes.DoesNotExist:
            v = Votes(user = request.user, slide = current_slide, value = 0)
            v.save()

    good = Votes.objects.filter(slide = current_slide, value = 0).count()
    bad = Votes.objects.filter(slide = current_slide, value = 1).count()
    total = good + bad
    if (total == 0):
        total = 1
        good = 1
    
    return {'good': good, 'bad':bad, 'total':total}


@login_required
def next_page(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
    try:
        slide = Slides.objects.get(slide_text = current.slide_name, page = current.page + 1)
        current.page += 1
        current.save()
    except Slides.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def prev_page(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
    try:
        slide = Slides.objects.get(slide_text = current.slide_name, page = current.page - 1)
        current.page -= 1
        current.save()
    except Slides.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def curr_page(request):
    mycurr = get_object_or_404(Current, owner = request.user, active=1)
    lecturer = Slides.objects.get(slide_text = mycurr.slide_name, page=1).lecturer
    try:
        lecture_curr = Current.objects.get(slide_name = mycurr.slide_name, owner = lecturer)
        mycurr.page = lecture_curr.page
        mycurr.save()
    except Slides.DoesNotExist:
        return HttpResponseNotFound()
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def vote_up(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
    current_slide = Slides.objects.get(slide_text = current.slide_name, page= current.page)

    if (Current.objects.get(owner = current_slide.lecturer, slide_name = current_slide.slide_text).page >= current.page):
        try:
            v = Votes.objects.get(user = request.user, slide = current_slide)
            v.value = 0
        except Votes.DoesNotExist:
            v = Votes(user = request.user, slide = current_slide, value = 0)
        v.save()
        v.send_notification(get_votes(request))
    else:
        pass
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def vote_down(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
    current_slide = Slides.objects.get(slide_text = current.slide_name, page= current.page)

    if (Current.objects.get(owner = current_slide.lecturer, slide_name = current_slide.slide_text).page >= current.page):
        try:
            v = Votes.objects.get(user = request.user, slide = current_slide)
            v.value = 1
        except Votes.DoesNotExist:
            v = Votes(user = request.user, slide = current_slide, value = 1)
        v.save()
        v.send_notification(get_votes(request))
    else:
        pass    
    return HttpResponseRedirect(reverse('slides:lecture'))


'''
@login_required
def home(request):
    return HttpResponseRedirect(reverse('slides:index', args=[request.user.username]))
'''
def login(request):
    return HttpResponseRedirect('/login/')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

