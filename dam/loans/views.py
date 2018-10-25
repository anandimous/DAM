from django.shortcuts import render
from django.contrib import messages 
from django import forms
from django.http import Http404
from django.urls import reverse
import forms
# Create your views here.

def checkIfItemAvailable(request, item_id): 
    if request.method == 'POST':
        form= validForm(request.POST)
        if form.is_valid():
            try: 
                item= Item.objects.with_availability().get(id=item_id)
            except Item.DoesNotExist:
                raise Http404()
            if item.available> 0:
                messages.success(request, 'Your item has been reserved! You can pick it up from Baldy 19')
                return redirect('/details',input_id=item_id)
            else:
                messages.error(request, 'Your item was not reserved. Please go back and reserve the item again.'
                return redirect(reverse('/inventory:index'))
        else:
            raise Http404()



