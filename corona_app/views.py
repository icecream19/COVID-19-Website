from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def worldwide(request):
    return render(request, 'worldwide.html')

def measures(request):
    return render(request, 'measures.html')
