from django import forms
from apps.hello.models import AppUser


class EditForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
