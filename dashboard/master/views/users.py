from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required

from ..models import UserDetail as MasterUser, User, PartnerGallery
#from django.contrib.auth.models import User
from ..forms import UserForm
from home.models import PartnerForm
from dashboard.services.models import (StichingCategory, StichingFinish,
                                       StichingPattern, StichingService, OrderTracking)
from commons.services import STICHING_SERVICES
from commons.user_role import authenticated_user,allowed_users,admin_only
from django.contrib.auth.hashers import make_password

from commons.roles import ROLE_CHOICES, ROLE_CHOICES_MAP



@login_required
@admin_only
def list_user(request):  
    userm = MasterUser()
    users_list = userm.list(request)
    return render(request, "list_users.html", context={'users' : users_list})


@login_required
@admin_only
def add_user(request):
    if request.method == "POST":
        try:            
            new_user = MasterUser()
            new_user.create(request)
            return redirect(list_user)
        except IntegrityError as e:
            return render(request, 'add_user.html', {'message' : 'user already exists'})
    return render(request, 'add_user.html', context={})



@login_required(login_url="/login/")
@admin_only
def selected_users(request, role):
    
    role_type = ROLE_CHOICES_MAP[role]
    users = User.objects.filter(role=role_type,is_active=1).all()
    return render(request, "selected-users.html", context={'users' : users, 'role' : role})

@login_required
@admin_only
def edit_user(request, id):
    user = User.objects.get(id=id)
    userm ={}
    if user.is_details_added:
        userm = MasterUser.objects.get(user_id=id)
    
    if request.method == "POST":
        new_user = User.objects.get(id=id)
        new_user.first_name = request.POST.get('first_name', '')
        new_user.last_name = request.POST.get('last_name', '')
        new_user.email = request.POST.get('email', '')
        new_user.password = request.POST.get('password', '')
        new_user.role = request.POST.get('role', '')
        new_user.mobile_no = request.POST.get('mobile_no', '')
        new_user.save()

        
        
        userm = MasterUser.objects.get(user_id=id)
        userm.mobile_no = request.POST.get('mobile_no', '')
        userm.gender = request.POST.get('gender', '')
        userm.dob = request.POST.get('dob', '')
        userm.address = request.POST.get('address', '')
        userm.land_mark = request.POST.get('landmark', '')
        userm.city = request.POST.get('city', '')
        userm.state = request.POST.get('state', '')
        userm.country = request.POST.get('country', '')
        userm.pincode = request.POST.get('pincode', '')
        userm.longitude = request.POST.get('longitude', '')
        userm.latitude = request.POST.get('lattitude', '')
        userm.modified_on = datetime.now()
        userm.modified_by = request.user.id
        userm.save()
        return redirect("list_user")
    return render(request, 'edit_user.html', context={'users' : userm, 'user': user})


@login_required
@admin_only
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(reverse('list_user'))


@login_required
@admin_only
def edit_partner(request):
    current_user = request.user
    id = current_user.id
    user = User.objects.get(id=id)
    if request.method == "POST":
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.mobile_no = request.POST.get('mobile_no', '')
        user.password = request.POST.get('password', '')
        user.save()

        userm = MasterUser.objects.get(user=user)
        userm.gender = request.POST.get('gender', '')
        userm.address = request.POST.get('address', '')
        userm.location = request.POST.get('city', '')
        userm.pincode = request.POST.get('pincode', '')
        userm.modified_on = datetime.now()
        userm.modified_by = request.user.id
        userm.save()

        partner = PartnerForm.objects.get(user=user)
        partner.service_type = request.POST.get('servicesTypePartnerForm','').strip()
        partner.service_name = request.POST.get('servicesPartnerForm','').strip()
        partner.organization_name = request.POST.get('organization','').strip()       
        partner.save() 

    return render(request, 'edit_partner.html', context={'user' : user, 'services':STICHING_SERVICES})


@login_required
@admin_only
def partner_my_work(request):
    current_user = request.user
    images = PartnerGallery.objects.filter(user=current_user).all()
    if request.method == "POST":
        gallery = PartnerGallery()
        gallery.user_id = current_user.id
        gallery.image = request.FILES.get('itemImage', '')
        gallery.title = request.POST.get('imagetitle', '')
        gallery.save()
    return render(request, 'my_work.html',{'images': images})



@login_required
@admin_only
def customer_report(request):
    return render(request, 'customer_report.html')


@login_required
@admin_only
def designer_performance(request):
    return render(request, 'designer_pereformance.html')





# --- reference 
# year = 2012
# month = 09
# Departure_Date.objects.filter(date_from__year__gte=year,
#                               date_from__month__gte=month,
#                               date_to__year__lte=year,
#                               date_to__month__lte=month)
@login_required
@admin_only
def order_report(request):
    order_booked_count = OrderTracking.objects.filter(created_on__month=2,status_name='Order Booked').count()
    order_canceled_count = OrderTracking.objects.filter(created_on__month=2,status_name='Order Canceled').count()
    order_delivered_count = OrderTracking.objects.filter(created_on__month=2,status_name='Delivered').count()
    return render(request, 'order_report.html',{'order_booked_count': order_booked_count, 'order_canceled_count': order_canceled_count, 'order_delivered_count': order_delivered_count })



