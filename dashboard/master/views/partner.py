from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required

from ..models import UserDetail as MasterUser, User, PartnerGallery

from home.models import PartnerForm

from commons.services import STICHING_SERVICES
from commons.user_role import authenticated_user,allowed_users,admin_only
from django.contrib.auth.hashers import make_password




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

    return render(request, 'partner/edit_partner.html', context={'user' : user, 'services':STICHING_SERVICES})


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
    return render(request, 'partner/my_work.html',{'images': images})



@login_required
def partner_gallery(request):
    patners = User.objects.filter(role=4,is_active=1)
    
    return render(request, 'partner_gallery.html',{'patners':patners})


@login_required
def remove_gallery(request, id):
    image = PartnerGallery.objects.get(id=id)
    image.delete()
    return redirect(partner_my_work)


