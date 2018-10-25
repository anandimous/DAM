from django.shortcuts import render
from django.contrib import messages 
from django import forms
# Create your views here.

class UserInputForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()


def checkIfItemAvailable(request): 
    if request.method == 'POST':
        if(Item.objects.with_availability().get(id=item_id).available() > 0:
            messages.success(request, 'Your item has been reserved! You can pick it up from Baldy 19')
        else:
            messages.error(request, 'Your item was not reserved. Please go back and reserve the item again.')

    return redirect('/results/details')

