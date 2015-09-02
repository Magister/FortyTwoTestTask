from django import forms
from apps.hello.models import AppUser
from apps.hello.widgets import DatePickerWidget


class EditForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'
        widgets = {
            'date_of_birth': DatePickerWidget,
        }

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            current_class = self.fields[field].widget.attrs.get('class', '')
            self.fields[field].widget.attrs['class'] = (
                current_class + ' form-control').strip()
