from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta  
from commons.roles import is_user_superadmin
from .models import MeasurementGroups
from commons.user_role import authenticated_user,allowed_users,admin_only




@login_required
@admin_only
def add(request):
    groups = MeasurementGroups.objects.all().order_by('category')
    if request.method == "POST":
        category = request.POST.get('category', '')
        name = request.POST.get('name', '').strip()
        try:
            check_items = MeasurementGroups.objects.get(category=category, name=name)
        except:
            create_groups= MeasurementGroups()
            create_groups.category= category
            create_groups.name = name
            create_groups.save()         
    return render(request, "measurement_groups.html",{'groups':groups})
    

@login_required
@admin_only
def edit(request, id):
    select_list = MeasurementGroups.objects.get(id=id)
    groups = MeasurementGroups.objects.all().order_by('category')
    if request.method == "POST":
        select_list.category = request.POST.get('category', '')
        select_list.name = request.POST.get('name', '').strip()
        select_list.save()
        return redirect(add)
    return render(request, "edit_measurement_groups.html", {'groups':groups, 'select_list' : select_list})


@login_required
@admin_only
def delete(request, id):
    delete_items = MeasurementGroups.objects.get(id=id)
    delete_items.delete()
    return redirect(add)

