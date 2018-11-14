from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan, Client


@login_required
def showDash(request):
    res = ItemReservation.objects.filter(is_active=True)
    loans = ItemLoan.objects.filter(returned_at__isnull=True)
    args = {'reserves': res,
            'returns': loans}
    return render(request, 'dashboard/dashboard.html', args)
