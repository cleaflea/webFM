from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url('^index/$', 'douban.views.index'),
                       )