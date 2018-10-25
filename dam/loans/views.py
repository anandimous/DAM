from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from ..inventory import models
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan, Client
from django.contrib import messages 
from django.urls import reverse
from dam.core import forms

@login_required
def reservations(request, reservation_id):
    try:
        reservation = ItemReservation.objects.get(id=reservation_id, is_active=True)
    except ItemReservation.DoesNotExist:
        raise Http404('Reservation Not Possible!')
    args = {'reserved': reservation,
            'user': request.user
            }
    if request.method=="POST":
        if "Approve" in request.POST:
            itemloaned = ItemLoan.objects.create(item=reservation.item, client=reservation.client, approved_by=request.user)

            reservation.is_active = False
            reservation.save()
            messages.success(request, 'Loan Successful!')
            return HttpResponseRedirect('/loans/loanslist')
        if "Decline" in request.POST:
            messages.success(request, 'Loan Declined!')
            reservation.is_active = False
            reservation.save()
            return HttpResponseRedirect('/loans/loanslist')
    return render(request, 'loans/loanItem.html', args)

def allres(request):
    res = ItemReservation.objects.filter(is_active=True)

    args = {'reserves': res}
    return render(request, 'loans/allReservations.html', args)

def allrets(request):
    rets = ItemLoan.objects.filter(returned_at__isnull=True)
    args = {'returns': rets}
    return render(request, 'loans/allReturns.html', args)

client= Client.objects.create {
    first_name= form.cleaned_data['first_name']
    last_name= form.cleaned_data['last_name']
    email= form.cleaned_data['email']
}

def checkIfItemAvailable(request, item_id): 
    if request.method == 'POST':
        form= validForm(request.POST)
        if form.is_valid():
            try: 
                item= Item.objects.with_availability().get(id=item_id)
            except Item.DoesNotExist:
                raise Http404()
            if item.available> 0:
                ItemReservation.object.create(
                    item=item,
                    client=client,
                )
                messages.success(request, 'Your item has been reserved! You can pick it up from Baldy 19')
                return redirect('/details',input_id=item_id)
            else:
                messages.error(request, 'Your item was not reserved. Please go back and reserve the item again.')
                return redirect(reverse('inventory:index'))
        else:
            raise Http404()



