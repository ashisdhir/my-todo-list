from django import forms
from .models import todo


class todoNewForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ('description', )
