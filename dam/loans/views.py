from django.shortcuts import render

from django.http import Http404
from ..inventory import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dam.loans.models import ItemReservation, ItemLoan


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
            itemloaned = ItemLoan()
            itemloaned.item = reservation.item
            itemloaned.client = reservation.client
            itemloaned.approved_by = request.user
            itemloaned.save()
            reservation.is_active = False
            reservation.save()
            messages.success(request, 'Loan Successful!')
        if "Decline" in request.POST:
            messages.success(request, 'Loan Declined!')
        reservation.is_active = False
        reservation.save()
    return render(request, 'loans/loanItem.html', args)
