from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from . import views 

app_name = 'slides'
urlpatterns = [
    url(r'^profile/', views.index),
    url(r'^login/', views.login),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^select/([a-zA-Z0-9_]+)', views.select, name='select'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^lecture/next_page/', views.next_page, name='next page'),
    url(r'^lecture/prev_page/', views.prev_page, name='previous page'),
    url(r'^lecture/curr_page/', views.curr_page, name='current page'),
    url(r'^lecture/vote_up/', views.vote_up, name='vote up'),
    url(r'^lecture/vote_down/', views.vote_down, name='vote down'),
    #lecture/ must be at the bottom otherwise it will always be matched first
    url(r'^lecture/', views.lecture, name='lecture'),
]
