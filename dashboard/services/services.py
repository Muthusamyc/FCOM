from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from dashboard.master.models import User

from commons.user_role import authenticated_user,allowed_users,admin_only
from commons.roles import is_user_superadmin
from .models import Service

@login_required
@admin_only
def add(request):
    services = Service.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        user= get_object_or_404(User, pk=request.user.id)
        obj = Service(name=name, description=description, created_by= user)        
        obj.save()
        return redirect(add)            
    return render(request, "service/add.html", { 'items' : services})
    
@login_required
@admin_only
def edit(request, id):
    service_to_edit = Service.objects.get(id=id)
    if request.method == "POST":
        user= get_object_or_404(User, pk=request.user.id)
        service_to_edit.name = request.POST['name']
        service_to_edit.description = request.POST['description']
        service_to_edit.created_by = user
        service_to_edit.save()
        return redirect(add)
    return render(request, 'service/edit.html', { 'selected_service' : service_to_edit})

@login_required
@admin_only
def delete(request, id):    
    service = Service.objects.get(id=id)
    service.delete()
    return redirect(add)