from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^index/$', 'doubanAuth.views.nocaptcha_login_user'),
                       url(r'^test/$', 'doubanAuth.views.test'),
                       url(r'^loginajax/$', 'doubanAuth.views.loginAjax'),
                       url(r'^getsongajax/$', 'doubanAuth.views.getSongAjax'),
)