from django.shortcuts import render, redirect, get_object_or_404

from dashboard.master.models import User

from commons.services import STICHING_SERVICES, get_service_class
from django.contrib.auth.decorators import login_required
from commons.user_role import authenticated_user,allowed_users,admin_only

@login_required
@admin_only
def add(request, page):
    selected_cls = get_service_class(page.lower())
    selected_objs = selected_cls.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        user= get_object_or_404(User, pk=request.user.id)
        obj = selected_cls(name=name, created_by= user)        
        obj.save()
        return redirect(add, page)            
    return render(request, "add_stitching_category.html", { 'items' : selected_objs, 'page_name' : page.capitalize()})
    
@login_required
@admin_only
def edit(request, page, id):
    selected_cls = get_service_class(page.lower())
    selected_obj = selected_cls.objects.get(id=id)
    if request.method == "POST":
        user= get_object_or_404(User, pk=request.user.id)
        selected_obj.name = request.POST['name']
        selected_obj.created_by = user
        selected_obj.save()
        return redirect(add, page)
    return render(request, 'edit_stitching_category.html', { 'selected_service' : selected_obj, 'page_name' : page.capitalize()})

@login_required
@admin_only
def delete(request, page, id):
    selected_cls = get_service_class(page.lower())
    service = selected_cls.objects.get(id=id)
    service.delete()
    return redirect(add, page)