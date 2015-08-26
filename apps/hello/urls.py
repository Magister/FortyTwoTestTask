from django.conf import settings
from django.conf.urls import patterns, url
from apps.hello import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^' + settings.MEDIA_URL.lstrip('/') + r'(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,
          'show_indexes': True
          }
         ),
    )
