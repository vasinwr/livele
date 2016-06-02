from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from .models import Current, PDF, Votes, PDFForm 
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
#from .forms import PDFForm


# Create your views here.

@login_required
def index(request):
    user_courses = request.user.groups.exclude(name = 'Lecturer').exclude(name = 'Student').values_list('name', flat=True)
    return render(request, 'slides/index.html', {'courses': user_courses})


@login_required
def course_index(request, course):
    # Handle file upload
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
           form.save()
            # Redirect to the document list after POST
           return HttpResponseRedirect(reverse('slides:course_index'))
    else:
        form = PDFForm()  # A empty, unbound form

    # Load documents for the list page
    course_group = Group.objects.get(name = course)
    documents = PDF.objects.filter(course = course_group)
    '''
    return render_to_response(
        'slides/course_index.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
    '''
    # Render list page with the documents and the form
    if(request.user.groups.filter(name = 'Lecturer').count() == 1):
        return render(request, 'slides/course_index.html', {'course': course, 'lecturer':True, 'documents': documents, 'form': form})
    else:
        return render(request, 'slides/course_index.html', {'course': course, 'documents': documents, 'form': form})

@login_required
def select(request, key):
#deactive all other actives.
    try:
        other = Current.objects.get(owner = request.user, active=1)
        other.active = 0
        other.save()
    except Current.DoesNotExist:
        pass

    try:
	curr_pdf = PDF.objects.get(pk = key)
        current = Current.objects.get(owner = request.user, pdf = curr_pdf)
        current.active = 1
        current.save()
    except Current.DoesNotExist:
        current = Current(owner = request.user, pdf = curr_pdf, page=1, active=1)
        current.save()

    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def lecture(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
    pdf = current.pdf

    votes = get_votes(request);
    good = votes['good']
    bad = votes['bad']
    total = votes['total']
    if(request.user.groups.filter(name = 'Lecturer').count() == 1):
#felix pass in arguments here::: maybe you want to use pdffile instead of filename and course
        return render(request, 'slides/lecture.html', {'filename': pdf.filename, 'course':pdf.course, 'pageCount':current.page, 'lecturer':True, 'votes_amplified':bad *100 / total, 'votes_rest': good*100/total})
    else:
        return render(request, 'slides/lecture.html', {'filename': pdf.filename, 'course':pdf.course, 'pageCount':current.page, 'student':True, 'votes_amplified':bad*100/total, 'votes_rest': good*100/ total})

def get_votes(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
    curr_pdf = current.pdf

    canVote = curr_pdf.current_page >= current.page
    if(canVote and request.user.groups.filter(name = 'Student').count() == 1):
        try:
            myvote = Votes.objects.get(user = request.user, pdf = curr_pdf, page = current.page)
        except Votes.DoesNotExist:
            v = Votes(user = request.user, pdf = curr_pdf, page = current.page, value = 0)
            v.save()

    good = Votes.objects.filter(pdf = curr_pdf, page = current.page, value = 0).count()
    bad = Votes.objects.filter(pdf = curr_pdf, page = current.page, value = 1).count()
    total = good + bad
    if (total == 0):
        total = 1
        good = 1
    
    return {'good': good, 'bad':bad, 'total':total}


@login_required
def next_page(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
# felix is there a check in pdf to check if page > last page?
#    if (current.page +1 <= current.pdf.**lastpage**)
#	current.page +=1
#	current.save()
#	if(request.user.groups.filter(name = 'Lecturer').count() == 1):
#	    current.pdf.current_page += 1
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def prev_page(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
    if (current.page > 1):
	current.page -= 1
	current.save
	if(request.user.groups.filter(name = 'Lecturer').count() == 1):
	    current.pdf.current_page -= 1
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def curr_page(request):
    mycurr = get_object_or_404(Current, owner = request.user, active=1)
    mycurr.page = mycurr.pdf.current_page
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def vote_up(request):
    current = get_object_or_404(Current, owner = request.user, active=1)

    if (current.pdf.current_page >= current.page):
        try:
            v = Votes.objects.get(user = request.user, pdf = current.pdf, page = current.page)
            v.value = 0
        except Votes.DoesNotExist:
            v = Votes(user = request.user, pdf = current.pdf, page = current.page, value = 0)
        v.save()
        v.send_notification(get_votes(request))
    else:
        pass
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def vote_down(request):
    current = get_object_or_404(Current, owner = request.user, active=1)

    if (current.pdf.current_page >= current.page):
        try:
            v = Votes.objects.get(user = request.user, pdf = current.pdf, page = current.page)
            v.value = 1
        except Votes.DoesNotExist:
            v = Votes(user = request.user, pdf = current.pdf, page = current.page, value = 1)
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

