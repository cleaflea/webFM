from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from webdouban import settings

admin.autodiscover()
from webdouban import views as webdoubanview

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'webdouban.views.home', name='home'),
                       # url(r'^webdouban/', include('webdouban.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', webdoubanview.index),
)

urlpatterns += patterns('',
                        url(r'^douban/', include('douban.urls')),
                        url(r'^doubanstatic/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.DOUBAN_STATIC_PATH}),
)

urlpatterns += patterns('',
                        url(r'^auth/', include('doubanAuth.urls')),
                        url(r'^authstatic/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.AUTH_STATIC_PATH}),

)

urlpatterns += patterns('',
                        url(r'^captcha/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.CAPTCHA_PATH}),
                        )