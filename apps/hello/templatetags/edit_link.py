from django import template
from django.core.urlresolvers import reverse
from django.db.models import Model

register = template.Library()


@register.simple_tag
def edit_link(obj):
    if isinstance(obj, Model):
        admin_url = reverse(
            'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name),
            args=(obj.pk,))
        link_tag = '<a href="%s">admin</a>' % (admin_url,)
    else:
        link_tag = ''
    return link_tag
