from django import forms

class reserveItemForm(forms.Form):
    
    email = forms.EmailField()
    item_id= forms.IntegerField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean_email(self):
        email=self.cleaned_data['email']
        if not email.endswith('@buffalo.edu'):
            raise forms.ValidationError('Invalid email! Please use your @buffalo.edu email address to reserve items.')
        return email
