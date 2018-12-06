from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from ..inventory.models import Item
from django.contrib.auth.decorators import login_required
from dam.loans.models import ItemReservation, ItemLoan, Client
from django.contrib import messages 
from django.urls import reverse
from django.utils import timezone
import dam.loans.forms as reserve_form
from django.db.models import Q


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
            ItemLoan.objects.create(item=reservation.item, client=reservation.client, approved_by=request.user)

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
        loan.returned_at = timezone.now()
        loan.save()
        messages.success(request, 'Item Returned!')
        return HttpResponseRedirect(reverse('loans:allrets'))
    return render(request, 'loans/returnItem.html', args)


@login_required
def allres(request):
    res = ItemReservation.objects.filter(is_active=True)
    query = request.GET.get('q')
    if query is not None:
        res = res.filter(
            Q(item__name__icontains=query)
            | Q(item__description__icontains=query)
            | Q(client__first_name__icontains=query)
            | Q(client__last_name__icontains=query)
            | Q(client__email__icontains=query)
        )
    return render(request, 'loans/allReservations.html', {'reserves': res})


@login_required
def allrets(request):
    rets = ItemLoan.objects.filter(returned_at__isnull=True)
    query = request.GET.get('q')
    if query is not None:
        rets = rets.filter(
            Q(item__name__icontains=query)
            | Q(item__description__icontains=query)
            | Q(client__first_name__icontains=query)
            | Q(client__last_name__icontains=query)
            | Q(client__email__icontains=query)
        )
    return render(request, 'loans/allReturns.html', {'returns': rets})

def checkIfItemAvailable(request, item_id): 
    if request.method == 'POST':
        form = reserve_form.reserveItemForm(request.POST)
        if form.is_valid():
            try: 
                item = Item.objects.with_availability().get(id=item_id)
            except Item.DoesNotExist:
                raise Http404('The selected item is not available.')
            if item.available > 0:
                client = Client.objects.create(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                )
                ItemReservation.objects.create(
                    item=item,
                    client=client,
                    reservation_ends= timezone.now() + timezone.timedelta(days=5)
                )
                messages.success(request, 'The item has been reserved! You can pick it up from Baldy 19.')
                return redirect(reverse('inventory:item-details', kwargs={'item_id': item.id}))
            else:
                messages.error(request, 'The item you tried to reserve is not available.')
                return redirect(reverse('inventory:item-details', kwargs={'item_id': item.id}))
        else:
            raise Http404('Form input is invalid')
