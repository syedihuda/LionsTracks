__author__ = 'Syed'

from django.conf.urls import patterns, url
from lionstracksapp import views

urlpatterns = patterns('',
    # ex: /lionstracksapp/
    url(r'^$', views.index, name='index'),
    # ex: /lionstracksapp/dataupload/
    url(r'^dataupload/$', views.dataupload, name='dataupload'),
)
