from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan, Client
from django.db.models import Q


@login_required
def showDash(request):
    user = request.user.email
    res = ItemReservation.objects.filter(is_active=True)
    query = request.GET.get(request)
    if query is not None:
        res = res.filter(
            Q(client__user__email__exact=query)
            |Q(client__user__first__name__exact=query)
        )
    loan = ItemLoan.objects.filter(returned_at__isnull=True)
    query = request.GET.get(request)
    if query is not None:
        loan = loan.filter(
            Q(client__user__email__exact=query)
            | Q(client__user__first__name__exact=query)
        )
    args = {'reserves': res,
            'returns': loan}
    return render(request, 'dashboard/dashboard.html', args)
