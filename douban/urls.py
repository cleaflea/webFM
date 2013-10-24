from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^index/$', 'douban.views.index'),
                       )