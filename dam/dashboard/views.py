from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan
from django.db.models import Q
from django.utils import timezone

@login_required
def showDash(request):
    user = request.user
    reservations = (
        ItemReservation.objects
        .filter(reservation_ends__gte=timezone.now())
        .filter(Q(client__user=user) | Q(client__email=user.email))
    )
    loans = (
        ItemLoan.objects
        .filter(returned_at__isnull=True)
        .filter(Q(client__user=user) | Q(client__email=user.email))
    )
    return render(request, 'dashboard/dashboard.html', {
        'reserves': reservations,
        'returns': loans,
    })
