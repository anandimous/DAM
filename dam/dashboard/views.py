from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan, Client
from django.db.models import Q


@login_required
def showDash(request):
    user = request.user.email
    res = ItemReservation.objects.filter(is_active=True)
    query = request.GET.get('q')
    if query is not None:
        res = res.filter(
            Q(client__email=query)
            |Q(client__first__name=query)
        )
    loan = ItemLoan.objects.filter(returned_at__isnull=True)
    query = request.GET.get('q')
    if query is not None:
        loan = loan.filter(
            Q(client__email=query)
            | Q(client__first__name=query)
        )
    args = {'reserves': res,
            'returns': loan}
    return render(request, 'dashboard/dashboard.html', args)
