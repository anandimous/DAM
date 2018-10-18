from django.shortcuts import render

# Create your views here.
def showDash(request):
    return render(request, 'dashboard/dashboard.html')
