from django import forms
from .models import Category


class CategoryFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)
    query = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'input-field col s12',
               'placeholder': 'Search by Name or Description',
               'title':'Please fill out this field.',
               'style': 'background-color:var(--white); -webkit-box-sizing: border-box; padding: 5px;'}))

    def __init__(self, *args, **kwargs):
        super(CategoryFilterForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()
