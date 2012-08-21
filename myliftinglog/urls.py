from django.conf.urls import patterns, include, url
from django.conf import settings


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^myliftinglog/$', 'liftinglog.views.index'),
    url(r'^myliftinglog/(?P<log_id>\d+)/$', 'liftinglog.views.detail'),
    url(r'^myliftinglog/progress/(?P<lift>\w+)/$', 'liftinglog.views.progress'),
    url(r'^myliftinglog/register/$', 'liftinglog.views.registration'),
    url(r'^myliftinglog/add/$', 'liftinglog.views.addLog'),
    url(r'^myliftinglog/login/$', 'liftinglog.views.signin'),
    url(r'^myliftinglog/logout/$', 'liftinglog.views.signout'),
    url(r'^myliftinglog/about/$', 'liftinglog.views.about'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )