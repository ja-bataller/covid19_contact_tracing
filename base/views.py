from typing import ContextManager
from django.forms.widgets import PasswordInput
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import UserAccount
from .forms import SignUpForm


def index(request):
    return render(request, 'index.html')

def scan(request):

    if request.method == 'POST':
        contact_number = request.POST.get('scanned_id')
        location = request.POST.get('location')

        print("ID: ", contact_number)
        print("Location: ", location)

        return render(request, 'scan.html')

    return render(request, 'scan.html')

def createSuperUser(username, password, email, firstName = "", lastName = ""):
    invalidInputs = ["", None]

    if username.strip() in invalidInputs or password.strip() in invalidInputs:
        return None

    user = User(
        username = username,
        email = email,
        first_name = firstName,
        last_name = lastName,
    )
    user.set_password(password)
    user.is_superuser = False
    user.is_staff = True
    user.save()

    return user

def login_page(request):
    page = 'login'

    if request.method == 'POST':
          contact_number = request.POST.get('contact_number')
          password = request.POST.get('password')

          try:
               user = User.objects.get(username=contact_number)
          except:
                context={'page': page, 'response': "not_found"}
                return render(request, 'login.html', context)
        
          user = authenticate(request, username=contact_number, password=password)

          if user is None:
                context={'page': page, 'response': "invalid_credentials"}
                return render(request, 'login.html', context)

          if user.is_superuser == True:
           
                if user is not None:
                    login(request, user)
                    return redirect('admin_home')

                else:
                    context={'page': page, 'response': "invalid_credentials"}
                    return render(request, 'login.html', context)
          else:

                if user is not None:
                    login(request, user)
                    return redirect('client_dashboard')

                else:
                    context={'page': page, 'response': "invalid_credentials"}
                    return render(request, 'login.html', context)

    context={'page': page}
    return render(request, 'login.html', context)

def signup_page(request):
    page='signup'
    form=SignUpForm()

    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        password = request.POST.get('password')
        email = request.POST.get('email_address')

        form=SignUpForm(request.POST)
        
        try:
            user = User.objects.get(username=contact_number)
        except:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.status = "inactive"
                obj.save()

                createSuperUser(username=contact_number,password=password, email=email)
                user = authenticate(request, username=contact_number, password=password)

            if user is not None:
                login(request, user)
                return redirect('client_dashboard')
            else:
                print("Error: Not Logged-in")

        context={'form': form, 'page': page, 'response': "exist"}
        return render(request, 'login.html', context)


    context={'form': form, 'page': page}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')


# ADMINS VIEW

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_home(request):
    current_user = request.user
    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    user_count = UserAccount.objects.all().count()
    active_user_count = UserAccount.objects.filter(status='active').count()
    pui_user_count = UserAccount.objects.filter(status='pui').count()

    context={'client_name': client_name, 'client_id' : client_id,'user_count' : user_count, 'active_user_count' : active_user_count, 'pui_user_count' : pui_user_count}
    return render(request, 'admin_home.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_users_dashboard(request):
    current_user = request.user
    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    user = UserAccount.objects.all()

    context = {'users' : user, 'client_name': client_name, 'client_id': client_id}
    return render(request, 'admin_users_dashboard.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_user_info(request, id):
    current_user = request.user
    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    user = UserAccount.objects.get(contact_number=id)
    gender = user.gender

    if request.method == 'POST':
        # gender = request.POST.get('contact_number')
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        email_address = request.POST.get('email_address')
        home_address = request.POST.get('home_address')

        User.objects.filter(username = id).update(email = email_address)

        UserAccount.objects.filter(contact_number = id).update(full_name = full_name)
        UserAccount.objects.filter(contact_number = id).update(gender = gender)
        UserAccount.objects.filter(contact_number = id).update(email_address = email_address)
        UserAccount.objects.filter(contact_number = id).update(home_address = home_address)

        current_user = request.user
        user_info = UserAccount.objects.get(contact_number=current_user)

        client_name = user_info.full_name
        client_id = user_info.contact_number

        user = UserAccount.objects.get(contact_number=id)
        gender = user.gender

        context = {'user_info': user, 'gender': gender, 'client_name': client_name, 'client_id': client_id}

        return render(request, 'admin_user_info.html', context)

    context = {'user_info': user, 'gender': gender, 'client_name': client_name, 'client_id': client_id}

    return render(request, 'admin_user_info.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_pui_dashboard(request):
    current_user = request.user
    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    context={'client_name': client_name, 'client_id': client_id}
    return render(request, 'admin_pui_dashboard.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_about(request):
    current_user = request.user
    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    context={'client_name': client_name, 'client_id': client_id}
    return render(request, 'admin_about.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='client_dashboard')
def client_error(request):

    # GET CURRENT LOGGED IN USER
    current_user = request.user

    # GET THE INFORMATION OF CURRENT LOGGED IN USER

    #  variable = Model Name - Database Field = Data to Search
    user_info = UserAccount.objects.get(contact_number=current_user)
    
    client_name = user_info.full_name
    client_id = user_info.contact_number

    # Variable - Dictionary
    context={'client_name': client_name, 'client_id': client_id}

    # Return Render the HTML Page and pass the Dictionary data
    return render(request, 'client_error.html', context)


# CLIENT VIEW
@login_required(login_url='login')
@staff_member_required(login_url='client_error')
def client_dashboard(request):
    return render(request, 'client_dashboard.html')

@login_required(login_url='login')
@staff_member_required(login_url='client_error')
def client_contact(request):
    return render(request, 'client_contact.html')

@login_required(login_url='login')
@staff_member_required(login_url='client_error')
def client_about(request):
    return render(request, 'client_about.html')

@login_required(login_url='login')
@staff_member_required(login_url='admin_home')
def admin_error(request):
    current_user = request.user
    user_info = UserAccount.objects.get(contact_number=current_user)
    
    client_name = user_info.full_name
    client_id = user_info.contact_number

    context={'client_name': client_name, 'client_id': client_id}

    return render(request, 'admin_error.html',context)