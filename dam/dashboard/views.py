from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan, Client
from django.db.models import Q

@login_required
def showDash(request):
    user = request.user
    reservations = (
        ItemReservation.objects
        .filter(is_active=True)
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
