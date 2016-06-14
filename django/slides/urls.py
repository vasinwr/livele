from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from . import views 

app_name = 'slides'
urlpatterns = [
    url(r'^api/register/$', views.register),
    url(r'^api/login/$', views.login),
    url(r'^api/logout/$', views.logout),
    
    url(r'^clicker_next/', views.clicker_next),
    url(r'^clicker_prev/', views.clicker_prev),
    url(r'^clicker_menu/', views.clicker_menu),

    url(r'^getpdf/', views.pdf_view),
    url(r'^returnsomejson/', views.returnsomejson),
#    url(r'^profile/', views.index),
    url(r'^login/', views.login),
    url(r'^logout/$', views.logout_view, name='logout'),
#    url(r'^$', views.index, name='index'),
    url(r'^course_list/', views.course_list, name='course list'),
    url(r'^select_lecture/([a-zA-Z0-9_]+)', views.select_lecture, name='select lecture'),
    url(r'^lecture_list/([a-zA-Z0-9_]+)', views.lecture_list, name='lecture list'),
    url(r'^get_pdf/', views.get_pdf, name='get pdf'),
    url(r'^lecture/get_page_questions/', views.get_page_questions, name='get page questions'),
    url(r'^lecture/get_qform/', views.get_qform, name='get qform'),
    url(r'^lecture/get_curr_page/', views.get_curr_page, name='get curr page'),
    url(r'^lecture/get_mood/', views.get_mood, name='get mood'),
    url(r'^lecture/get_speed/', views.get_speed, name='get speed'),
    url(r'^lecture/check_speed/', views.get_speed, name='check speed'),
    url(r'^lecture/go_next_page/', views.go_next_page, name='go next page'),
    url(r'^lecture/go_prev_page/', views.go_prev_page, name='go previous page'),
    url(r'^lecture/go_curr_page/', views.go_curr_page, name='go current page'),
    url(r'^lecture/vote_up/', views.vote_up, name='vote up'),
    url(r'^lecture/vote_down/', views.vote_down, name='vote down'),
    url(r'^lecture/too_slow/', views.too_slow, name='too slow'),
    url(r'^lecture/too_fast/', views.too_fast, name='too fast'),
    url(r'^lecture/question/', views.question, name='question'),
    url(r'^lecture/qvote/([a-zA-Z0-9_]+)', views.qvote, name='qvote'),
    url(r'^lecture/show_questions/', views.show_questions, name='show questions'),
    url(r'^trigger_anything/', views.trigger_anything, name='trigger anything'),
    #lecture/ must be at the bottom otherwise it will always be matched first
#    url(r'^lecture/', views.lecture, name='lecture'),
]
