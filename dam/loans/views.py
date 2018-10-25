from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from ..inventory import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dam.loans.models import ItemReservation, ItemLoan
from datetime import datetime
from django.urls import reverse

@login_required
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


@login_required
def returns(request, loan_id):
    try:
        loan = ItemLoan.objects.get(id=loan_id, returned_at__isnull=True)
    except ItemLoan.DoesNotExist:
        raise Http404('Return Not Possible!')
    args = {'loan': loan,
            'user': request.user
            }
    if request.method == "POST":
        loan.returned_at = datetime.utcnow()
        loan.save()
        messages.success(request, 'Item Returned!')
        return HttpResponseRedirect(reverse('loans:allrets'))
    return render(request, 'loans/returnItem.html', args)


def allres(request):
    res = ItemReservation.objects.filter(is_active=True)

    args = {'reserves': res}
    return render(request, 'loans/allReservations.html', args)


def allrets(request):
    rets = ItemLoan.objects.filter(returned_at__isnull=True)
    args = {'returns': rets}
    return render(request, 'loans/allReturns.html', args)
