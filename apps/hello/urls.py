from django.conf import settings
from django.conf.urls import patterns, url
from apps.hello import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^requestlog$', views.requestlog, name='requestlog'),
    url(r'^edit_request$', views.edit_request, name='edit_request'),
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
