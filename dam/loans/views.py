from django.shortcuts import render

from django.http import Http404
from ..inventory import models
from dam.loans.models import ItemReservation, ItemLoan
from dam.loans.forms import LoansForm


def reservations(request, reservation_id):
    try:
        reserved = ItemReservation.objects.get(id=reservation_id)
    except ItemReservation.DoesNotExist:
        raise Http404('Reservation Does not Exist!')


    args = {'reserved': reserved,
            'user':request.user
            }
    return render(request, 'loans/loanItem.html', args)

def get(self, request):
    form = LoansForm()
    return render(request,'loans/loanItem.html', {'form': form})

def post(self, request):
    form = LoansForm(request.post)
    args = {'form': form,
                }
    return render(request, 'loans/loanItem.html', args)
