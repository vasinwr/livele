from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse;
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from .models import Current, PDF, Votes, PDFForm, Question, QuestionForm, Question_Vote, Speed
from django.contrib.auth.models import User, Group
from channels import Group as Channel_Group
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Count
#from .forms import PDFForm
import os
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


from .utils import json_response, token_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import Token

# Create your views here.
@csrf_exempt
@token_required
def clicker_full(request):
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    pdf = current.pdf
    notification = {
        "type": 'clicker',
        "nav": 'full',
    }
    Channel_Group(str(pdf.pk)).send({
       "text": json.dumps(notification),
    })
    return JsonResponse({'ack':False})

@csrf_exempt
@token_required
def clicker_next(request):
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    pdf = current.pdf
    notification = {
        "type": 'clicker',
        "nav": 'next',
    }
    Channel_Group(str(pdf.pk)).send({
       "text": json.dumps(notification),
    })
    return JsonResponse({'ack':False})

@csrf_exempt
@token_required
def clicker_prev(request):
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    pdf = current.pdf
    notification = {
        "type": 'clicker',
        "nav": 'prev',
    }
    Channel_Group(str(pdf.pk)).send({
       "text": json.dumps(notification),
    })
    return JsonResponse({'ack':False})

@csrf_exempt
@token_required
def clicker_menu(request):
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    pdf = current.pdf
    notification = {
        "type": 'clicker',
        "nav": 'menu',
    }
    Channel_Group(str(pdf.pk)).send({
       "text": json.dumps(notification),
    })
    return JsonResponse({'ack':False})



def pdf_view(request):
    print (os.path.join(settings.MEDIA_ROOT, 'Backpropagation.pdf'))
    with open(os.path.join(settings.MEDIA_ROOT,'slides.pdf') ,'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        response['Access-Control-Allow-Headers'] = 'Range'
        response['Access-Control-Expose-Headers'] = 'Accept-Ranges, Content-Encoding, Content-Length, Content-Range'
        return response
    pdf.closed


@csrf_exempt
@token_required
def returnsomejson(request):
  #Votes.send_notif()
  return json_response({'x':'something'})

'''
@csrf_exempt
@token_required
def course_index(request, course):
    course_group = Group.objects.get(name = course)
    # Handle file upload
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.course = course_group
            pdf.lecturer = request.token.user
            pdf.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(course)
    else:
        form = PDFForm()  # A empty, unbound form

    # Load documents for the list page
    documents = PDF.objects.filter(course = course_group)

    return render_to_response(
        'slides/course_index.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

    # Render list page with the documents and the form
    if(request.token.user.groups.filter(name = 'Lecturer').count() == 1):
        return render(request, 'slides/course_index.html', {'course': course, 'lecturer':True, 'documents': documents, 'form': form})
    else:
        return render(request, 'slides/course_index.html', {'course': course, 'documents': documents, 'form': form})
'''

@csrf_exempt
@token_required
def course_list(request):
# returns a list of courses the user is subscribed to
# access c in course, c.pk, c.fields.name
    user_courses = serializers.serialize("json", request.token.user.groups.exclude(name = 'Lecturer').exclude(name = 'Student'))
    return JsonResponse(user_courses, safe = False)

@csrf_exempt
@token_required
def lecture_list(request, course):
# returns a list of lectures(pdfs) in the selected course
# access doc in documents, doc.pk, doc.fields.filename, doc.fields.someotherfield
    course_group = Group.objects.get(pk = course)
    documents = serializers.serialize("json", PDF.objects.filter(course = course_group))
    return JsonResponse(documents, safe=False)


@csrf_exempt
@token_required
def select_lecture(request, key):
# selects PDF with the key and marks as the user's active
# returns true after selected
#deactive all other actives.
    try:
        other = Current.objects.get(owner = request.token.user, active=1)
        other.active = 0
        other.save()
    except Current.DoesNotExist:
        pass

    try:
        curr_pdf = get_object_or_404(PDF, pk = key)
        current = Current.objects.get(owner = request.token.user, pdf = curr_pdf)
        current.active = 1
        current.save()
    except Current.DoesNotExist:
        current = Current(owner = request.token.user, pdf = curr_pdf, page=1, active=1)
        current.save()

    return JsonResponse({'ack':True})

'''
@csrf_exempt
@token_required
def lecture(request):
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    pdf = current.pdf

    votes = get_votes(request);
    good = votes['good']
    bad = votes['bad']
    total = votes['total']

    if(request.token.user.groups.filter(name = 'Lecturer').count() == 1):
        return render(request, 'slides/lecture.html', {'pdffile': pdf.pdffile.url, 'pageCount':current.page, 'lecturer':True, 'votes_amplified':bad *100 / total, 'votes_rest': good*100/total})
    else:
        question_form = QuestionForm()
        curr_qs = Question.objects.filter(pdf = current.pdf, page = current.page)
        displayQ = curr_qs.annotate(votes = Count('question_vote')).order_by('-votes')
        return render(request, 'slides/lecture.html', {'pdffile': pdf.pdffile.url, 'pageCount':current.page, 'student':True, 'qform':question_form, 'questions': displayQ, 'votes_amplified':bad*100/total, 'votes_rest': good*100/ total})
'''

@csrf_exempt
@token_required
def get_pdf(request):
    current = get_object_or_404(Current, owner = request.token.user, active=1)
#    user = User.objects.get(username = 'lecturer1')
#    current = Current.objects.get(owner = user, active = 1)
#    print (os.path.join(settings.MEDIA_ROOT, current.pdf.pdffile))
    with open(os.path.join(settings.MEDIA_ROOT, str(current.pdf.pdffile)) ,'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename= current.pdf.filename '
        response['Access-Control-Allow-Headers'] = 'Range'
        response['Access-Control-Expose-Headers'] = 'Accept-Ranges, Content-Encoding, Content-Length, Content-Range'
        return response
    pdf.closed


@csrf_exempt
@token_required
def get_page_questions(request):
# returns list of questions on user's page on the pdf, can be used q.pk, q.fields.pk, q.fields.vote
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    curr_qs = Question.objects.filter(pdf = current.pdf, page = current.page)
    qs = curr_qs.annotate(votes = Count('question_vote')).order_by('-votes').values()
    displayQ = json.dumps(list(qs), cls=DjangoJSONEncoder)
    return JsonResponse(displayQ, safe=False)



@csrf_exempt
@token_required
def get_qform(request):
# returns a blank question form if the user can vote
# returns false otherwise
    if (current.pdf.current_page >= current.page):
        current = get_object_or_404(Current, owner = request.token.user, active=1)
        question_form = QuestionForm()
        return JsonResponse({'qform':question_form})
    else:
        return JsonResponse({'qform':False})


@csrf_exempt
@token_required
def get_curr_page(request):
# returns current page number for the user
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    return JsonResponse({'page':current.page})


@csrf_exempt
@token_required
def get_mood(request):
# return mood status as percentages
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    curr_pdf = current.pdf

    canVote = curr_pdf.current_page >= current.page
    if(canVote and request.token.user.groups.filter(name = 'Student').count() == 1):
        try:
            myvote = Votes.objects.get(user = request.token.user, pdf = curr_pdf, page = current.page)
        except Votes.DoesNotExist:
            v = Votes(user = request.token.user, pdf = curr_pdf, page = current.page, value = 0)
            v.save()

    good = Votes.objects.filter(pdf = curr_pdf, page=current.page, value = 0).count()
    bad = Votes.objects.filter(pdf = curr_pdf, page=current.page, value = 1).count()
    total = good + bad
    if (total == 0):
        total = 1
        good = 1
    
    return JsonResponse({'good': good*100/total, 'bad': bad*100/total})

def send_mood(pdf, page):
# sends mood status as percentages

    good = Votes.objects.filter(pdf = pdf, page=page, value = 0).count()
    bad = Votes.objects.filter(pdf = pdf, page=page, value = 1).count()
    total = good + bad
    if (total == 0):
        total = 1
        good = 1
    
    notification = {
        "type": 'bar',
        "page": page,
        "green_bar": good*100/total,
        "red_bar": bad*100/total,
    }
    Channel_Group(str(pdf.pk)).send({
       "text": json.dumps(notification),
    })

@csrf_exempt
@token_required
def get_speed(request):
# return speed status
    current = get_object_or_404(Current, owner = request.token.user, active=1)

    slow = Speed.objects.filter(pdf = current.pdf, value = 0).count()
    fast = Speed.objects.filter(pdf = current.pdf, value = 1).count()
    au = Current.objects.filter(pdf = current.pdf).count()
    
    return JsonResponse({'audience': au-1, 'slow': slow, 'fast': fast})

@csrf_exempt
@token_required
def check_speed(request):
# return speed status for this user. 0 is nothing, 1 is slow, 2 is fast.
    current = get_object_or_404(Current, owner = request.token.user, active=1)

    status = 0
    try:
        s = Speed.objects.get(user = request.token.user, pdf = current.pdf)
        status = s.value +1
    except Speed.DoesNotExist:
        pass
    
    return JsonResponse({'speed': status})

def send_speed(pdf):
# sends speed status

    slow = Speed.objects.filter(pdf = pdf, value = 0).count()
    fast = Speed.objects.filter(pdf = pdf, value = 1).count()
    au = Current.objects.filter(pdf = pdf).count()
    
    notification = {
        "type": 'speed',
        "audience": au-1,
        "slow": slow,
        "fast": fast,
    }
    Channel_Group(str(pdf.pk)).send({
       "text": json.dumps(notification),
    })



@csrf_exempt
@token_required
def go_next_page(request):
# user moves to page+1. need to check if this is valid before calling. use pdf.js checkmax in frontend.
# returns updated page number
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    current.page +=1
    current.save()
    if(request.token.user == current.pdf.lecturer):
        current.pdf.current_page = current.page
        current.pdf.save()
        notification = {
            "type": 'nav',
        }
        Channel_Group(str(current.pdf.pk)).send({
           "text": json.dumps(notification),
        })
    return JsonResponse({'page':current.page})


@csrf_exempt
@token_required
def go_prev_page(request):
# user moves to page-1. 
# returns updated page number
    current = get_object_or_404(Current, owner = request.token.user, active=1)
    if (current.page > 1):
        current.page -= 1
        current.save()
        if(request.token.user == current.pdf.lecturer):
          current.pdf.current_page = current.page
          current.pdf.save()
          notification = {
              "type": 'nav',
          }
          Channel_Group(str(current.pdf.pk)).send({
             "text": json.dumps(notification),
          })
    return JsonResponse({'page':current.page})


@csrf_exempt
@token_required
def go_curr_page(request):
# user jumps to lecturer's current page. 
# returns updated page number
    mycurr = get_object_or_404(Current, owner = request.token.user, active=1)
    mycurr.page = mycurr.pdf.current_page
    mycurr.save()
    return JsonResponse({'page':mycurr.page})


@csrf_exempt
@token_required
def vote_up(request):
# user votes up on his current slide. 
# returns true if voted, false otherwise.
    current = get_object_or_404(Current, owner = request.token.user, active=1)

    if (current.pdf.current_page >= current.page):
        try:
            v = Votes.objects.get(user = request.token.user, pdf = current.pdf, page = current.page)
            v.value = 0
        except Votes.DoesNotExist:
            v = Votes(user = request.token.user, pdf = current.pdf, page = current.page, value = 0)
        v.save()
        send_mood(current.pdf, current.page)

        return JsonResponse({'ack':True})
    else:
        pass
    return JsonResponse({'ack':False})


@csrf_exempt
@token_required
def vote_down(request):
# user votes down on his current slide. 
# returns true if voted, false otherwise.
    current = get_object_or_404(Current, owner = request.token.user, active=1)

    if (current.pdf.current_page >= current.page):
        try:
            v = Votes.objects.get(user = request.token.user, pdf = current.pdf, page = current.page)
            v.value = 1
        except Votes.DoesNotExist:
            v = Votes(user = request.token.user, pdf = current.pdf, page = current.page, value = 1)
        v.save()
        send_mood(current.pdf, current.page)

        return JsonResponse({'ack':True})
    else:
        pass    
    return JsonResponse({'ack':False})

@csrf_exempt
@token_required
def too_slow(request):
# user votes up on his current slide. 
# returns true if voted, false otherwise.
    current = get_object_or_404(Current, owner = request.token.user, active=1)

    try:
        s = Speed.objects.get(user = request.token.user, pdf = current.pdf)
        if (s.value == 0):
            s.delete()
        else:
            s.value = 0
            s.save()
    except Speed.DoesNotExist:
        s = Speed(user = request.token.user, pdf = current.pdf, value = 0)
        s.save()
    send_speed(current.pdf)

    return JsonResponse({'ack':True})


@csrf_exempt
@token_required
def too_fast(request):
# user votes up on his current slide. 
# returns true if voted, false otherwise.
    current = get_object_or_404(Current, owner = request.token.user, active=1)

    try:
        s = Speed.objects.get(user = request.token.user, pdf = current.pdf)
        if (s.value == 1):
            s.delete()
        else:
            s.value = 1
            s.save()
    except Speed.DoesNotExist:
        s = Speed(user = request.token.user, pdf = current.pdf, value = 1)
        s.save()
    send_speed(current.pdf)

    return JsonResponse({'ack':True})


@csrf_exempt
@token_required
def question(request):
# user asks a question on his current slide. 
# returns true if question asked, false otherwise.

    current = get_object_or_404(Current, owner = request.token.user, active=1)
    ques = None
    if request.method == 'POST':
        ques = request.body

    if (current.pdf.current_page >= current.page):
        q = Question(user = request.token.user, pdf = current.pdf, page = current.page, text = ques)
        q.save()
        notification = {
            "type": 'question',
        }
        Channel_Group(str(current.pdf.pk)).send({
            "text": json.dumps(notification),
        })
        return JsonResponse({'ack':True})
    else:
        pass
    return JsonResponse({'ack':False})


@csrf_exempt
@token_required
def qvote(request, question):
# user votes up the question with given private key.
# returns an ack for checking.
    q = get_object_or_404(Question, pk = question)

    try:
        v = Question_Vote.objects.get(user = request.token.user, question = q)
    except Question_Vote.DoesNotExist:
        v = Question_Vote(user = request.token.user, question = q)
        v.save()
        notification = {
            "type": 'question',
        }
        Channel_Group(str(q.pdf.pk)).send({
            "text": json.dumps(notification),
        })

    return JsonResponse({'ack':question})


@csrf_exempt
@token_required
def show_questions(request):
# for lecturer to see all questions asked on his current lecture, from all pages.
# returns a list of questions that can be used -- q.fields.text , q.fields.page, q.fields.vote etc
    current = get_object_or_404(Current, owner = request.token.user, active=1)

    curr_qs = Question.objects.filter(pdf = current.pdf)
    qs = curr_qs.annotate(votes = Count('question_vote')).order_by('-votes').values()
    displayQ = json.dumps(list(qs), cls=DjangoJSONEncoder)

    return JsonResponse(displayQ, safe=False)

@csrf_exempt
def trigger_anything(request):
    pdf = PDF.objects.get(filename = "CH1")
    notification = {
        "type": 'question',
    }
    Channel_Group(str(pdf.pk)).send({
        "text": json.dumps(notification),
    })
    return JsonResponse({'fucking':'piece of shit'})



#-------------------------------------------------------------------------------------------------
#login / logout stuff
#-------------------------------------------------------------------------------------------------


'''
@csrf_exempt
@token_required
def home(request):
    return HttpResponseRedirect(reverse('slides:index', args=[request.token.user.username]))
'''
'''
def login(request):
    return HttpResponseRedirect('/login/')
'''
@csrf_exempt
@token_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username is not None and password is not None:
            try:
                user = User.objects.create_user(username, None, password)
            except IntegrityError:
                return json_response({
                    'error': 'User already exists'
                }, status=400)
            token = Token.objects.create(user=user)
            return json_response({
                'token': token.token,
                'username': user.username
            })
        else:
            return json_response({
                'error': 'Invalid Data'
            }, status=400)
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if username is not None and password is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return json_response({
                        'token': token.token,
                        'username': user.username,
                        'user_is_lec': user.groups.filter(name = 'Lecturer').count()
                    })
                else:
                    return json_response({
                        'error': 'Invalid User'
                    }, status=400)
            else:
                return json_response({
                    'error': 'Invalid Username/Password'
                }, status=400)
        else:
            return json_response({
                'error': 'Invalid Data'
            }, status=400)
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)


@csrf_exempt
@token_required
def logout(request):
    if request.method == 'POST':
        request.token.delete()
        return json_response({
            'status': 'success'
        })
    elif request.method == 'OPTIONS':
        return json_response({})
    else:
        return json_response({
            'error': 'Invalid Method'
        }, status=405)
