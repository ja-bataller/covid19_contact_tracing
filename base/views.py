from typing import ContextManager
from django.forms.widgets import PasswordInput
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import check_password
from .models import UserAccount
from .models import UserLogs
from .models import ActiveLogs
from .forms import SignUpForm

import datetime
import pytz

import serial

def rfid_scanner():
    try:
        ser = serial.Serial('COM5', baudrate = 9600, timeout=1)\

    except serial.SerialException:
        error = "No connection to the device could be established"
        print (error)
        return error

    while 1 :
        arduinoData = ser.readline().decode('ascii')
        if arduinoData == "":
            pass
        else:
            print(arduinoData)
            return arduinoData

# INDEX PAGE
def index(request):
    return render(request, 'index.html')

# QR CODE SCANNER PAGE
def scan(request):

    if request.method == 'POST':
        id = request.POST.get('scanned_id')
        store = request.POST.get('location')

        # date_today = datetime.datetime.today().strftime('%m/%d/%Y')
        # time_today = datetime.datetime.today().strftime("%I:%M %p")
        date_today = datetime.datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime('%m/%d/%Y')
        time_today = datetime.datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime("%I:%M %p")

        try:
            user_status = UserAccount.objects.get(contact_number=id)

            if user_status.status == "active":

                time_in = UserLogs(full_name=user_status.full_name, contact_number=id, branch="Manila", date=date_today, location=store, time_in=time_today)
                time_in.save()

                if ActiveLogs.objects.filter(contact_number=id).exists():
                    user_active_log = ActiveLogs.objects.get(contact_number=id)

                    if user_active_log.date == date_today:

                        print("existing and update")
                        ActiveLogs.objects.filter(contact_number=id).update(location=store)
                        ActiveLogs.objects.filter(contact_number=id).update(time_in=time_today)

                        return render(request, 'scan.html')

                    else:
                
                        # IF DATE IS NOT TODAY THEN , PROCESS
                        ActiveLogs.objects.filter(contact_number=id).update(location=store)
                        ActiveLogs.objects.filter(contact_number=id).update(date=date_today)
                        ActiveLogs.objects.filter(contact_number=id).update(time_in=time_today)

                        return render(request, 'scan.html')

                else:
                    print("create new log")
                    new_activelog = ActiveLogs(full_name=user_status.full_name, contact_number=id, branch="Manila", date=date_today, location=store, time_in=time_today)
                    new_activelog.save()

                    return render(request, 'scan.html')

            else:
                print("Alert - User is a PUI user.")
                return render(request, 'scan.html', {"response" : "pui"})

        except:
            print("Error - User not found.")
            return render(request, 'scan.html', {"response" : "unknown"})

        # print("User name:", user_status.full_name)
        # print("ID:", contact_number)
        # print("Store:", store)
        # print("Today's date:", date_today)
        # print("Current Time:", time_today)

    return render(request, 'scan.html')

# RFID SCANNER PAGE
def tap(request):

    scanned_id = rfid_scanner()

    if request.method == 'POST':
        store = request.POST.get('location')
        id = request.POST.get('scanned_id')

        print(store)
        print(id.replace(" ", ""))

        # date_today = datetime.datetime.today().strftime('%m/%d/%Y')
        # time_today = datetime.datetime.today().strftime("%I:%M %p")
        date_today = datetime.datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime('%m/%d/%Y')
        time_today = datetime.datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime("%I:%M %p")

        try:
            user_status = UserAccount.objects.get(rfid=id.replace(" ", ""))

            if user_status.status == "active":

                time_in = UserLogs(full_name=user_status.full_name, contact_number=user_status.contact_number, branch="Manila", date=date_today, location=store, time_in=time_today)
                time_in.save()

                if ActiveLogs.objects.filter(contact_number=user_status.contact_number).exists():
                    user_active_log = ActiveLogs.objects.get(contact_number=user_status.contact_number)

                    if user_active_log.date == date_today:

                        print("existing and update")
                        ActiveLogs.objects.filter(contact_number=user_status.contact_number).update(location=store)
                        ActiveLogs.objects.filter(contact_number=user_status.contact_number).update(time_in=time_today)

                        return render(request, 'scan.html')

                    else:
                
                        # IF DATE IS NOT TODAY THEN , PROCESS
                        ActiveLogs.objects.filter(contact_number=user_status.contact_number).update(location=store)
                        ActiveLogs.objects.filter(contact_number=user_status.contact_number).update(date=date_today)
                        ActiveLogs.objects.filter(contact_number=user_status.contact_number).update(time_in=time_today)

                        return render(request, 'scan.html')

                else:
                    print("create new log")
                    new_activelog = ActiveLogs(full_name=user_status.full_name, contact_number=user_status.contact_number, branch="Manila", date=date_today, location=store, time_in=time_today)
                    new_activelog.save()

                    return render(request, 'scan.html')

            else:
                print("Alert - User is a PUI user.")
                return render(request, 'scan.html', {"response" : "pui"})

        except:
            print("Error - User not found.")
            return render(request, 'scan.html', {"response" : "unknown"})

        # print("User name:", user_status.full_name)
        # print("ID:", contact_number)
        # print("Store:", store)
        # print("Today's date:", date_today)
        # print("Current Time:", time_today)

    return render(request, 'tap.html', {"id":scanned_id})

# CREATING A SUPER USER PROCESS
def createSuperUser(username, password, email, firstName="", lastName=""):
    invalidInputs = ["", None]

    if username.strip() in invalidInputs or password.strip() in invalidInputs:
        return None

    user = User(
        username=username,
        email=email,
        first_name=firstName,
        last_name=lastName,
    )
    user.set_password(password)
    user.is_superuser = False
    user.is_staff = True
    user.save()

    return user

# LOG-IN PAGE 
def login_page(request):
    page = 'login'

    if request.method == 'POST':
        contact_number =  request.POST.get('contact_number')
        password =  request.POST.get('password')

        try:
            user =  User.objects.get(username=contact_number)
        except:
            context = {'page': page, 'response': "not_found"}
            return render(request, 'login.html', context)

        user = authenticate(
            request, username=contact_number, password=password)

        if user is None:
            context = {'page': page, 'response': "invalid_credentials"}
            return render(request, 'login.html', context)

        if user.is_superuser == True:

            if user is not None:
                login(request, user)
                return redirect('admin_home')

            else:
                context = {'page': page, 'response': "invalid_credentials"}
                return render(request, 'login.html', context)
        else:

            if user is not None:
                login(request, user)
                return redirect('client_dashboard')

            else:
                context = {'page': page, 'response': "invalid_credentials"}
                return render(request, 'login.html', context)

    context = {'page': page}
    return render(request, 'login.html', context)

# SIGN-UP PAGE
def signup_page(request):
    page = 'signup'
    form = SignUpForm()

    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        password = request.POST.get('password')
        email = request.POST.get('email_address')

        form = SignUpForm(request.POST)

        try:
            user = User.objects.get(username=contact_number)
        except:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.status = "active"
                obj.save()

                createSuperUser(username=contact_number,
                                password=password, email=email)
                user = authenticate(
                    request, username=contact_number, password=password)

            if user is not None:
                login(request, user)
                return redirect('client_dashboard')
            else:
                print("Error: Not Logged-in")

        context = {'form': form, 'page': page, 'response': "exist"}
        return render(request, 'login.html', context)

    context = {'form': form, 'page': page}
    return render(request, 'login.html', context)

# LOG-OUT USER PROCESS
def logout_user(request):
    logout(request)
    return redirect('login')


# ADMINISTRATOR - ADMIN HOME PAGE
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_home(request):
    current_user = (request.user)
    currentpassword = (request.user.password)

    user_info = UserAccount.objects.get(contact_number=current_user)
    date_today = datetime.datetime.today().strftime('%m/%d/%Y')

    active_today = ActiveLogs.objects.filter(date=date_today)
    client_name = user_info.full_name
    client_id = user_info.contact_number

    user_count =  UserAccount.objects.all().count()
    active_user_count =  active_today.count()
    pui_user_count =  UserAccount.objects.filter(status='pui').count()

    if request.method == 'POST':
        oldClientPassword = request.POST.get('oldClientPassword')
        newClientPassword = request.POST.get('newClientPassword')

        match_check = check_password(oldClientPassword, currentpassword)
        if match_check:

            UserAccount.objects.filter(contact_number=current_user).update(
                password=newClientPassword)

            acc_change = User.objects.get(username=client_id)
            acc_change.set_password(newClientPassword)
            acc_change.save()

            context = {'client_name': client_name, 'client_id': client_id, 'user_count': user_count,
                       'active_user_count': active_user_count, 'pui_user_count': pui_user_count, 'active_today': active_today, 'response': "password changed"}
            return render(request, 'admin_home.html', context)

        else:
            context = {'client_name': client_name, 'client_id': client_id, 'user_count': user_count,
                       'active_user_count': active_user_count, 'pui_user_count': pui_user_count, 'active_today': active_today, 'response': "password mismatch"}
            return render(request, 'admin_home.html', context)

    context = {'client_name': client_name, 'client_id': client_id, 'user_count': user_count,
               'active_user_count': active_user_count, 'pui_user_count': pui_user_count, 'active_today': active_today}
    return render(request, 'admin_home.html', context)

# ADMINISTRATOR - TABLE OF CLIENT USERS
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_users_dashboard(request):
    current_user = request.user
    currentpassword = request.user.password

    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    user = UserAccount.objects.all()

    if request.method == 'POST':
        oldClientPassword = request.POST.get('oldClientPassword')
        newClientPassword = request.POST.get('newClientPassword')

        match_check = check_password(oldClientPassword, currentpassword)
        if match_check:

            UserAccount.objects.filter(contact_number=current_user).update(
                password=newClientPassword)

            acc_change = User.objects.get(username=client_id)
            acc_change.set_password(newClientPassword)
            acc_change.save()

            context = {'users': user, 'client_name': client_name,
                'client_id': client_id, 'response': 'password changed'}
            return render(request, 'admin_users_dashboard.html', context)

        else:
            context = {'users': user, 'client_name': client_name,
                'client_id': client_id, 'response': 'password mismatch'}
            return render(request, 'admin_users_dashboard.html', context)

    context = {'users': user, 'client_name': client_name,
               'client_id': client_id}
    return render(request, 'admin_users_dashboard.html', context)

# ADMINISTRATOR - CLIENT USER INFORMATIONS
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_user_info(request, id):
    current_user = request.user
    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    user = UserAccount.objects.get(contact_number=id)
    gender = user.gender

    user_history = UserLogs.objects.filter(contact_number = id)

    if request.method == 'POST':
        # gender = request.POST.get('contact_number')
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        email_address = request.POST.get('email_address')
        home_address = request.POST.get('home_address')

        User.objects.filter(username=id).update(email=email_address)

        UserAccount.objects.filter(contact_number=id).update(full_name=full_name)
        UserAccount.objects.filter(contact_number=id).update(gender=gender)
        UserAccount.objects.filter(contact_number=id).update(email_address=email_address)
        UserAccount.objects.filter(contact_number=id).update(home_address=home_address)

        current_user = request.user
        user_info = UserAccount.objects.get(contact_number=current_user)

        client_name = user_info.full_name
        client_id = user_info.contact_number

        user = UserAccount.objects.get(contact_number=id)
        gender = user.gender

        context = {'user_info': user, 'gender': gender, 'client_name': client_name, 'client_id': client_id, 'user_history': user_history, 'response': "success"}

        return render(request, 'admin_user_info.html', context)

    if user.status == "pui":
        context = {'user_info': user, 'gender': gender, 'client_name': client_name, 'client_id': client_id, 'user_history': user_history, 'response': "pui"}

        return render(request, 'admin_user_info.html', context)
    
    context = {'user_info': user, 'gender': gender, 'client_name': client_name, 'client_id': client_id, 'user_history': user_history, 'response': "active"}

    return render(request, 'admin_user_info.html', context)

# ADMINISTRATOR - UPDATING STATUS OF CLIENT USER TO PUI
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_user_pui(request, id):
    UserAccount.objects.filter(contact_number=id).update(status="pui")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# ADMINISTRATOR - UPDATING STATUS OF CLIENT USER TO ACTIVE
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_user_active(request, id):
    UserAccount.objects.filter(contact_number=id).update(status="active")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# ADMINISTRATOR - TABLE OF PUI CLIENT USERS
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_pui_dashboard(request):
    current_user = request.user
    currentpassword = request.user.password

    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    pui_user = UserAccount.objects.filter(status = "pui")

    if request.method == 'POST':
        oldClientPassword = request.POST.get('oldClientPassword')
        newClientPassword = request.POST.get('newClientPassword')

        match_check = check_password(oldClientPassword, currentpassword)

        if match_check:

            UserAccount.objects.filter(contact_number=current_user).update(
                password=newClientPassword)

            acc_change = User.objects.get(username=client_id)
            acc_change.set_password(newClientPassword)
            acc_change.save()

            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password changed', 'pui_user' : pui_user}
            return render(request, 'admin_pui_dashboard.html', context)

        else:
            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password mismatch', 'pui_user' : pui_user}
            return render(request, 'admin_pui_dashboard.html', context)

    context = {'client_name': client_name, 'client_id': client_id, 'pui_user' : pui_user}
    return render(request, 'admin_pui_dashboard.html', context)

# ADMINISTRATOR - ABOUT PAGE
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_error')
def admin_about(request):
    current_user = request.user
    currentpassword = request.user.password

    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    if request.method == 'POST':
        oldClientPassword = request.POST.get('oldClientPassword')
        newClientPassword = request.POST.get('newClientPassword')

        match_check = check_password(oldClientPassword, currentpassword)

        if match_check:

            UserAccount.objects.filter(contact_number=current_user).update(
                password=newClientPassword)

            acc_change = User.objects.get(username=client_id)
            acc_change.set_password(newClientPassword)
            acc_change.save()

            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password changed'}
            return render(request, 'admin_about.html', context)

        else:
            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password mismatch'}
            return render(request, 'admin_about.html', context)

    context = {'client_name': client_name, 'client_id': client_id}
    return render(request, 'admin_about.html', context)

# ADMINISTRATOR - ERROR LANDING PAGE
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='client_dashboard')
def client_error(request):

    # GET CURRENT LOGGED IN USER
    current_user = request.user
    currentpassword = request.user.password

    # GET THE INFORMATION OF CURRENT LOGGED IN USER

    #  variable = Model Name - Database Field = Data to Search
    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    if request.method == 'POST':
        oldClientPassword = request.POST.get('oldClientPassword')
        newClientPassword = request.POST.get('newClientPassword')

        match_check = check_password(oldClientPassword, currentpassword)

        if match_check:

            UserAccount.objects.filter(contact_number=current_user).update(
                password=newClientPassword)

            acc_change = User.objects.get(username=client_id)
            acc_change.set_password(newClientPassword)
            acc_change.save()

            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password changed'}
            return render(request, 'client_error.html', context)

        else:
            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password mismatch'}
            return render(request, 'client_error.html', context)

    # Variable - Dictionary
    context = {'client_name': client_name, 'client_id': client_id}

    # Return Render the HTML Page and pass the Dictionary data
    return render(request, 'client_error.html', context)


# CLIENT - CLIENT DASHBOARD PAGE
@login_required(login_url='login')
@staff_member_required(login_url='client_error')
def client_dashboard(request):

    # GET CURRENT LOGGED IN USER
    current_user = request.user
    currentpassword = request.user.password

    # GET THE INFORMATION OF CURRENT LOGGED IN USER

    #  variable = Model Name - Database Field = Data to Search
    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number
    client_status = user_info.status

    user_log = UserLogs.objects.filter(contact_number=current_user).filter(branch="Manila")

    if request.method == 'POST':
        oldClientPassword = request.POST.get('oldClientPassword')
        newClientPassword = request.POST.get('newClientPassword')

        match_check = check_password(oldClientPassword, currentpassword)

        if match_check:

            UserAccount.objects.filter(contact_number=current_user).update(
                password=newClientPassword)

            acc_change = User.objects.get(username=client_id)
            acc_change.set_password(newClientPassword)
            acc_change.save()

            context = {'client_name': client_name, 'client_id': client_id,'response': 'password changed'}
            return render(request, 'client_dashboard.html', context)

        else:
            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password mismatch'}
            return render(request, 'client_dashboard.html', context)

    # Variable - Dictionary
    context = {'client_name': client_name, 'client_id': client_id, 'user_log': user_log, 'client_status':client_status}

    # Return Render the HTML Page and pass the Dictionary data
    return render(request, 'client_dashboard.html', context)

# CLIENT - CONTACT PAGE
@login_required(login_url='login')
@staff_member_required(login_url='client_error')
def client_contact(request):
    current_user = request.user
    currentpassword = request.user.password

    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number
    client_email = user_info.email_address

    if request.method == 'POST':
        oldClientPassword = request.POST.get('oldClientPassword')
        newClientPassword = request.POST.get('newClientPassword')

        match_check = check_password(oldClientPassword, currentpassword)

        if match_check:

            UserAccount.objects.filter(contact_number=current_user).update(
                password=newClientPassword)

            acc_change = User.objects.get(username=client_id)
            acc_change.set_password(newClientPassword)
            acc_change.save()

            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password changed'}
            return render(request, 'client_contact.html', context)

        else:
            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password mismatch'}
            return render(request, 'client_contact.html', context)

    context = {'client_name': client_name, 'client_id': client_id, 'client_email': client_email}

    return render(request, 'client_contact.html', context)

#  CLIENT - ABOUT PAGE
@login_required(login_url='login')
@staff_member_required(login_url='client_error')
def client_about(request):
    current_user = request.user
    currentpassword = request.user.password

    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    if request.method == 'POST':
        oldClientPassword = request.POST.get('oldClientPassword')
        newClientPassword = request.POST.get('newClientPassword')

        match_check = check_password(oldClientPassword, currentpassword)

        if match_check:

            UserAccount.objects.filter(contact_number=current_user).update(
                password=newClientPassword)

            acc_change = User.objects.get(username=client_id)
            acc_change.set_password(newClientPassword)
            acc_change.save()

            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password changed'}
            return render(request, 'client_about.html', context)

        else:
            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password mismatch'}
            return render(request, 'client_about.html', context)

    context = {'client_name': client_name, 'client_id': client_id}
    return render(request, 'client_about.html', context)

#  CLIENT - ERROR LANDING PAGE
@login_required(login_url='login')
@staff_member_required(login_url='admin_home')
def admin_error(request):
    current_user = request.user
    currentpassword = request.user.password

    user_info = UserAccount.objects.get(contact_number=current_user)

    client_name = user_info.full_name
    client_id = user_info.contact_number

    user_log = UserLogs.objects.filter(contact_number=current_user).filter(branch="Manila")

    if request.method == 'POST':
        oldClientPassword = request.POST.get('oldClientPassword')
        newClientPassword = request.POST.get('newClientPassword')

        match_check = check_password(oldClientPassword, currentpassword)

        if match_check:

            UserAccount.objects.filter(contact_number=current_user).update(
                password=newClientPassword)

            acc_change = User.objects.get(username=client_id)
            acc_change.set_password(newClientPassword)
            acc_change.save()

            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password changed'}
            return render(request, 'client_about.html', context)

        else:
            context = {'client_name': client_name, 'client_id': client_id, 'response': 'password mismatch'}
            return render(request, 'client_about.html', context)

    context = {'client_name': client_name, 'client_id': client_id}

    return render(request, 'admin_error.html', context)