from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta  
from commons.roles import is_user_superadmin
from commons.services import get_preference_class
from commons.user_role import authenticated_user,allowed_users,admin_only

from .models import EstimatedConsultationDate


@login_required
@admin_only
def add(request, page):
    selected_cls = get_preference_class(page.lower())
    selected_objs = selected_cls.objects.all()
    if request.method == "POST":
        name = request.POST['name']        
        obj = selected_cls(name=name)        
        obj.save()
        return redirect(add, page)            
    return render(request, "add_preferences.html", { 'items' : selected_objs, 'page_name' : page.capitalize()})
    

@login_required
@admin_only
def edit(request, page, id):
    selected_cls = get_preference_class(page.lower())
    selected_objs = selected_cls.objects.get(id=id)
    if request.method == "POST":
        selected_objs.name = request.POST.get('name', '')
        selected_objs.save()
        
        return redirect(add, page)
    return render(request, "edit_preferences.html", { 'items' : selected_objs, 'page_name' : page.capitalize()})


@login_required
@admin_only
def delete(request, page, id):
    selected_cls = get_preference_class(page.lower())
    selected_objs = selected_cls.objects.get(id=id)
    selected_objs.delete()
    return redirect(add, page)


@login_required
@admin_only
def estimated_consultation_date(request):
    estimation_dates = EstimatedConsultationDate.objects.all().order_by('-id')
    service_modes = get_preference_class('service').objects.all()
    designer_preferences = get_preference_class("preference").objects.all()
    if request.method == "POST":
        service_mode_id = request.POST['service_mode']
        designer_preference_id = request.POST['designer_preference_mode']
        date = int(request.POST['est_dates'])
        estimated_date = EstimatedConsultationDate(
            service_mode_id = service_mode_id,
            designer_preference_mode_id = designer_preference_id,
            date = datetime.now() + timedelta(days=date)  
        )
        estimated_date.save()
        return redirect(estimated_consultation_date)
    return render(request, "estimated_consultation_date.html", {'estimation_dates' : estimation_dates, 'designer_preferences' : designer_preferences, 'service_modes' : service_modes})

@login_required
@admin_only
def edit_estimated_consultation_date(request, id):
    service_modes = get_preference_class('service').objects.all()
    designer_preferences = get_preference_class("preference").objects.all()
    estimation_dates = EstimatedConsultationDate.objects.get(id=id)
    
    if request.method == "POST":
        estimation_dates.service_mode_id = request.POST.get('service_mode', '')
        estimation_dates.designer_preference_mode_id = request.POST.get('designer_preference_mode', '')
        estimation_dates.date = request.POST.get('est_dates', '')
        estimation_dates.save()
        return redirect(estimated_consultation_date)
    return render(request, "edit_estimated_consultation_date.html", {'estimation_dates' : estimation_dates,'designer_preferences' : designer_preferences, 'service_modes' : service_modes})

@login_required
@admin_only
def delete_estimated_consultation_date(request, id):
    estimation_dates = EstimatedConsultationDate.objects.get(id=id)
    estimation_dates.delete()
    return redirect(estimated_consultation_date)