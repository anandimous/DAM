from django.shortcuts import render
from django.contrib import messages 

# Create your views here.
def render(request): 
    if request.method == 'POST':
        #if item exists
        #is available in database 
        if(Item.objects.with_availability().get(id=item_id).available() > 0 and Item.exists()):
            messages.set_level(request, messages.SUCCESS)
            messages.success(request, 'Your item has been reserved! You can pick it up from Baldy 19')
        else:
            messages.error(request, 'Your item was not reserved. Please go back and reserve the item again.')

