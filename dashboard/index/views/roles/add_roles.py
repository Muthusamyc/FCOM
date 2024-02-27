from django.shortcuts import render

def add_role(request):
    return render(request, "add_roles.html", context={})