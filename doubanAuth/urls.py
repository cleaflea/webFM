from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url('^index/$', 'doubanAuth.views.nocaptcha_login_user'),
                       url('^test/$', 'doubanAuth.views.test'),
)