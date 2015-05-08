__author__ = 'Syed'

from django.conf.urls import patterns, url
from lionstracksapp import views

urlpatterns = patterns('',
    # ex: /lionstracksapp/
    url(r'^$', views.index, name='index'),
    # ex: /lionstracksapp/dataupload/
    url(r'^dataupload/$', views.dataupload, name='dataupload'),
    #url(r'^login/$', views.user_login, name='user_login')
    url(r'^usermetrics/$', views.show_user_metrics, name='usermetrics'),
    url(r'^usermetricsdata/$', views.get_user_metrics_data, name='usermetricsdata'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^updateprofile/$', views.update_profile, name='updateprofile')
)
