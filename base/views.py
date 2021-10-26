from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def scan(request):
     return render(request, 'scan.html')

def login_signup(request):
     return render(request, 'login.html')

# ADMINS VIEW

def admin_home(request):
     return render(request, 'admin_home.html')

def admin_user_info(request):
     return render(request, 'admin_user_info.html')

def admin_active_dashboard(request):
     return render(request, 'admin_active_dashboard.html')

def admin_inactive_dashboard(request):
     return render(request, 'admin_inactive_dashboard.html')

def admin_pui_dashboard(request):
     return render(request, 'admin_pui_dashboard.html')

def admin_about(request):
     return render(request, 'admin_about.html')


# CLIENT VIEW

def client_dashboard(request):
     return render(request, 'client_dashboard.html')

def client_contact(request):
     return render(request, 'client_contact.html')

def client_about(request):
     return render(request, 'client_about.html')