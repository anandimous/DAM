from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from dam.inventory.models import Item
from dam.loans import forms
from dam.loans.models import ItemReservation, ItemLoan, Client


@permission_required('loans.change_itemreservation')
def reservations(request, reservation_id):
    try:
        reservation = ItemReservation.objects.get(id=reservation_id, is_active=True)
    except ItemReservation.DoesNotExist:
        raise Http404('Reservation Not Possible!')
    args = {'reserved': reservation,
            'user': request.user
            }
    if request.method == "POST":
        if "Approve" in request.POST:
            itemloaned = ItemLoan.objects.create(item=reservation.item, client=reservation.client, approved_by=request.user)

            reservation.is_active = False
            reservation.save()
            messages.success(request, 'Loan Successful!')
            return HttpResponseRedirect(reverse('loans:allres'))
        if "Decline" in request.POST:
            messages.success(request, 'Loan Declined!')
            reservation.is_active = False
            reservation.save()
            return HttpResponseRedirect(reverse('loans:allres'))
    return render(request, 'loans/loanItem.html', args)


@permission_required('loans.change_itemloan')
def returns(request, loan_id):
    try:
        loan = ItemLoan.objects.get(id=loan_id, returned_at__isnull=True)
    except ItemLoan.DoesNotExist:
        raise Http404('Return Not Possible!')
    args = {'loan': loan,
            'user': request.user
            }
    if request.method == "POST":
        loan.returned_at = timezone.now()
        loan.save()
        messages.success(request, 'Item Returned!')
        return HttpResponseRedirect(reverse('loans:allrets'))
    return render(request, 'loans/returnItem.html', args)


@permission_required('loans.view_itemreservation')
def allres(request):
    res = ItemReservation.objects.filter(is_active=True)

    args = {'reserves': res}
    return render(request, 'loans/allReservations.html', args)


@permission_required('loans.view_itemloan')
def allrets(request):
    rets = ItemLoan.objects.filter(returned_at__isnull=True)
    args = {'returns': rets}
    return render(request, 'loans/allReturns.html', args)


def checkIfItemAvailable(request, item_id): 
    if request.method == 'POST':
        form = forms.reserveItemForm(request.POST)
        if form.is_valid():
            try: 
                item = Item.objects.with_availability().get(id=item_id)
            except Item.DoesNotExist:
                raise Http404('The selected item is not available')
            if item.available > 0:
                client = Client.objects.create(
                    first_name = form.cleaned_data['first_name'],
                    last_name= form.cleaned_data['last_name'],
                    email= form.cleaned_data['email']
                )
                ItemReservation.objects.create(
                    item=item,
                    client=client,
                )
                messages.success(request, 'Your item has been reserved! You can pick it up from Baldy 19')
                return redirect('/inventory/details/' + str(item_id))
            else:
                messages.error(request, 'Your item was not reserved. Please go back and reserve the item again.')
                return redirect(reverse('inventory:index'))
        else:
            raise Http404('Form input is invalid')



