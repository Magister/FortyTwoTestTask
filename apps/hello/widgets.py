from django.forms import widgets


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
