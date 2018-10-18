from django.shortcuts import render

# Create your views here.
def showMain(request):
    return render(request, 'index/index.html')