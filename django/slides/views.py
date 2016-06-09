from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse;
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from .models import Current, PDF, Votes, PDFForm, Question, QuestionForm, Question_Vote
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Count
#from .forms import PDFForm
import os

# Create your views here.

def pdf_view(request):
    print (os.path.join(settings.MEDIA_ROOT, 'Backpropagation.pdf'))
    with open(os.path.join(settings.MEDIA_ROOT,'slides.pdf') ,'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        response['Access-Control-Allow-Headers'] = 'Range'
        response['Access-Control-Expose-Headers'] = 'Accept-Ranges, Content-Encoding, Content-Length, Content-Range'
        return response
    pdf.closed

def returnsomejson(request):
  return JsonResponse({'x':'something'})

@login_required
def index(request):
    user_courses = request.user.groups.exclude(name = 'Lecturer').exclude(name = 'Student').values_list('name', flat=True)
    return render(request, 'slides/index.html', {'courses': user_courses})


@login_required
def course_index(request, course):
    course_group = Group.objects.get(name = course)
    # Handle file upload
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.course = course_group
            pdf.lecturer = request.user
            pdf.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(course)
    else:
        form = PDFForm()  # A empty, unbound form

    # Load documents for the list page
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
        return render(request, 'slides/lecture.html', {'pdffile': pdf.pdffile.url, 'pageCount':current.page, 'lecturer':True, 'votes_amplified':bad *100 / total, 'votes_rest': good*100/total})
    else:
        question_form = QuestionForm()
        curr_qs = Question.objects.filter(pdf = current.pdf, page = current.page)
        displayQ = curr_qs.annotate(votes = Count('question_vote')).order_by('-votes')
        return render(request, 'slides/lecture.html', {'pdffile': pdf.pdffile.url, 'pageCount':current.page, 'student':True, 'qform':question_form, 'questions': displayQ, 'votes_amplified':bad*100/total, 'votes_rest': good*100/ total})

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
    current.page +=1
    current.save()
    if(request.user.groups.filter(name = 'Lecturer').count() == 1):
        current.pdf.current_page += 1
        current.pdf.save()
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def prev_page(request):
    current = get_object_or_404(Current, owner = request.user, active=1)
    if (current.page > 1):
        current.page -= 1
        current.save()
        if(request.user.groups.filter(name = 'Lecturer').count() == 1):
            current.pdf.current_page -= 1
            current.pdf.save()
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def curr_page(request):
    mycurr = get_object_or_404(Current, owner = request.user, active=1)
    mycurr.page = mycurr.pdf.current_page
    mycurr.save()
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

@login_required
def question(request):
    current = get_object_or_404(Current, owner = request.user, active=1)

    if (current.pdf.current_page >= current.page):
        dummy = Question(user = request.user, pdf = current.pdf, page = current.page, text = "")
        dummy.save()
        question = QuestionForm(request.POST, instance = dummy)
        question.save()
    else:
        pass
    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def qvote(request, question):
    q = get_object_or_404(Question, pk = question)

    try:
        v = Question_Vote.objects.get(user = request.user, question = q)
    except Question_Vote.DoesNotExist:
        v = Question_Vote(user = request.user, question = q)
        v.save()

    return HttpResponseRedirect(reverse('slides:lecture'))

@login_required
def show_questions(request):
    current = get_object_or_404(Current, owner = request.user, active=1)

    curr_qs = Question.objects.filter(pdf = current.pdf)
    displayQ = curr_qs.annotate(votes = Count('question_vote')).order_by('-votes')

    return render(request, 'slides/questions.html', {'questions':displayQ})


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

