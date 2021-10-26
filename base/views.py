from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def scan(request):
     return render(request, 'scan.html')

def login_signup(request):
     return render(request, 'login.html')