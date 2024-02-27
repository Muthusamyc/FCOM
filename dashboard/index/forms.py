from django import forms
from ..master import models
#from django.contrib.auth.models import User
from dashboard.master.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
################### Login Authentication Form ###################
from  django.contrib.auth.forms import AuthenticationForm
from commons.roles import CUSTOMER, PARTNER
from home.views import home
from dashboard.index.views import dashboard
from django.contrib import messages

class LoginForm(AuthenticationForm):
    email = forms.CharField(label="Username", max_length=30,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'})  )
    password = forms.CharField(label="Password", max_length=30,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))

                    

def authenticate_mobile_number(request, mobile_no=None, password=None):
    try:
        user = User.objects.get(mobile_no=mobile_no)
    except User.DoesNotExist:
        return None

    if user.check_password(password):
        return user

    return None                    

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request,email=email, password=password)
        
        if user and user.is_active:
            if user.role == CUSTOMER:
                logout(request)
                return redirect(home)
            else: 
                login(request, user) 
                return redirect(dashboard.index)
        else:
            return render(request, 'dashboard/login.html', {'message' : "Invalid Credentials"})
    return render(request, 'dashboard/login.html')
            

def partner_login(request):
    if request.method == 'POST':
        mobile_no = request.POST.get('mobile_no', '')
        password = request.POST.get('password', '')
        user = authenticate_mobile_number(request, mobile_no, password)
        if user and user.is_active and user.role == PARTNER:
            login(request, user) 
            return redirect(dashboard.index)
        else:
            return render(request, 'dashboard/partner_login.html', {'message' : "Invalid Credentials"})
    return render(request, 'dashboard/partner_login.html')
            
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')  
        try:
            user = User.objects.get(email=email)
            if user and user.is_active and user.role != CUSTOMER:
                user.password = make_password(password)
                user.save()
                messages.info(request, "Your Password Reset Successfully")
                return redirect(admin_login) 
            messages.info(request, "You are not an Authorized User")
            return render(request, 'dashboard/forget-password.html')
        except:
            messages.info(request, "Your account doesn't exist")
            return render(request, 'dashboard/forget-password.html')
    return render(request, 'dashboard/forget-password.html')

@login_required
def logout_dashboard_user(request):
    if request.user.is_authenticated:
        if request.user.role == PARTNER:
            logout(request)
            return redirect(partner_login)
        else:
            logout(request)
            return redirect(admin_login)
    
