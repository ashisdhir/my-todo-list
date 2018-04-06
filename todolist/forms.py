from django import forms
from .models import TodoTitle, TodoDetail, Author, Book
from django.forms.models import inlineformset_factory


BookFormSet = inlineformset_factory(Author, Book, fields=('title',))
# TodoDetailFormSet = inlineformset_factory(TodoTitle, TodoDetail, fields=('description', 'completed',))
TodoDetailFormSet = inlineformset_factory(TodoTitle, TodoDetail, fields=('description', 'completed',))
# class TodoNewForm(forms.ModelForm):
#     class Meta:
#         model = TodoTitle
#         fields = ('title',)
#
#     class Meta:
#         model = TodoDetail
#         fields = ('description', 'completed')


# class todoNewForm(forms.Form):
class TodoNewForm(forms.Form):
    title = forms.CharField(label='title', max_length=100, help_text='100 characters max.')
    description = forms.CharField(label='description')
    completed = forms.BooleanField(label='completed', required=False)


class TodoTitleForm(forms.ModelForm):
    class Meta:
        model = TodoTitle
        fields = ('user', 'title', 'created')
        widgets = {
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

todo_title_formset = forms.modelformset_factory(TodoTitle, fields=('user', 'title', 'created', ))

class TodoDetailForm(forms.ModelForm):
    class Meta:
        model = TodoDetail
        exclude = ()

# TodoDetailFormSet = inlineformset_factory(TodoTitle, TodoDetail, form=TodoDetailForm)

