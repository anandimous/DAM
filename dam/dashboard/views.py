from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan, Client
from django.db.models import Q


@login_required
def showDash(request):
    user = request.user.email
    cres = ItemReservation.objects.filter(is_active=True)
    query = request.GET.get('q')
    if query is not None:
        cres = cres.filter(
            Q(client__email=query)
            |Q(client__first__name=query)
        )
    loans = ItemLoan.objects.filter(returned_at__isnull=True)
    cloan = loans.filter(client__email=user)
    args = {'reserves': cres,
            'returns': cloan}
    return render(request, 'dashboard/dashboard.html', args)
