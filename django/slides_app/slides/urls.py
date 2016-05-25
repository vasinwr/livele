from django.conf.urls import url

from . import views 

app_name = 'slides'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^next_page/', views.next_page, name='next page'),
    url(r'^prev_page/', views.prev_page, name='previous page'),
]
