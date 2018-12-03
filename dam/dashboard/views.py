from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan, Client


@login_required
def showDash(request):
    user = request.user.email
    res = ItemReservation.objects.filter(is_active=True)
    cres= res.filter(client__email=user)
    loans = ItemLoan.objects.filter(returned_at__isnull=True)
    cloan = loans.filter(client__email=user)
    args = {'reserves': cres,
            'returns': cloan}
    return render(request, 'dashboard/dashboard.html', args)
