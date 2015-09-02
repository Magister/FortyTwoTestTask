from django.forms import widgets
from django.forms.util import flatatt
from django.template.defaultfilters import urlencode
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from fortytwo_test_task import settings


class DatePickerWidget(widgets.DateInput):

    class Media:
        js = (
            'libs/jquery-ui/jquery-ui.min.js',
            'hello/js/datepicker-widget.js',
        )
        css = {
            'all': ('libs/jquery-ui/themes/humanity/jquery-ui.min.css',)
        }

    def __init__(self, *args, **kwargs):
        super(DatePickerWidget, self).__init__(*args, **kwargs)
        current_class = self.attrs.get('class', '')
        self.attrs['class'] = (current_class + ' date-picker').strip()

    def render(self, name, value, attrs=None):
        html = super(DatePickerWidget, self).render(name, value, attrs)
        return html


class ImagePickerWidget(widgets.FileInput):

    class Media:
        js = (
            'hello/js/imagepicker-widget.js',
        )

    def __init__(self, *args, **kwargs):
        super(ImagePickerWidget, self).__init__(*args, **kwargs)
        current_class = self.attrs.get('class', '')
        self.attrs['class'] = (current_class + ' image-picker').strip()

    def render(self, name, value, attrs=None):
        input_field = super(ImagePickerWidget, self).render(name, value, attrs)
        img_attrs = {
            'id': 'img_' + attrs.get('id'),
            'alt': 'Photo not selected',
            'class': 'image-preview'
            }
        if str(value).strip():
            img_attrs['src'] = urlencode(settings.MEDIA_URL + str(value))
        rendered = format_html('<p><img{0} /></p>', flatatt(img_attrs))
        return rendered + input_field
