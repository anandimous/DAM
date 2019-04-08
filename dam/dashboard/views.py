from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan
from django.db.models import Q
from django.utils import timezone

@login_required
def showDash(request):
    user = request.user
    reservations = ItemReservation.objects.filter(
        user=user,
        reservation_ends__gte=timezone.now(),
    )
    loans = ItemLoan.objects.filter(
        user=user,
        returned_at__isnull=True,
    )
    return render(request, 'dashboard/dashboard.html', {
        'reserves': reservations,
        'returns': loans,
    })
