from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from apps.hello.forms import HelloAuthenticationForm

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('hello.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'authentication_form': HelloAuthenticationForm},
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('index')},
        name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
