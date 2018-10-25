from django.shortcuts import render
from django.contrib import messages 
from django import forms
from django.http import Http404
# Create your views here.

class validForm(forms.Form):
    
    email = forms.EmailField()
    item_id= forms.IntegerField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    
def valid_email(self):
    email=self.cleaned_data['email']
    if not email.endswith('@buffalo.edu'):
        raise ValidationError('Invalid email! Please use your @buffalo.edu email address to reserve items.')
    return email

def checkIfItemAvailable(request, item_id): 
    if request.method == 'POST':
        form= validForm(request.POST)
        if form.is_valid():
            if(Item.objects.with_availability().get(id=item_id).available() > 0:
                messages.success(request, 'Your item has been reserved! You can pick it up from Baldy 19')
                return redirect('/details',input_id=item_id)
            else:
                messages.error(request, 'Your item was not reserved. Please go back and reserve the item again.'
                return redirect('/inventory')
        else:
            raise Http404



