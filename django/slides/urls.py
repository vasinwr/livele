from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from . import views 

app_name = 'slides'
urlpatterns = [
#    url(r'^$', views.login, name='login_page'),
#    url(r'^login/$', views.login_user, name='login'),
#    url(r'^accounts/login/$', auth_views.login, {'template_name': 'slides/login.html'}),
    url(r'^accounts/profile/$', views.home),
    url(r'^$', views.index, name='index'),
    url(r'^index_lecturer/', views.lecturer, name='index lecturer'),
    url(r'^index_student/', views.student, name='index student'),
    url(r'^lecture/next_page/', views.next_page, name='next page'),
    url(r'^lecture/prev_page/', views.prev_page, name='previous page'),
    url(r'^lecture/vote_current/', views.vote_current, name='vote'),
    #lecture/ must be at the bottom otherwise it will always be matched first
    url(r'^lecture/(?P<isLecturer>[0-1])', views.lecture, name='lecture'),
]
