from django.shortcuts import render

def login(request):
    if request.method == "POST":
        userId = request.POST.get('userId', '')
        password = request.POST.get('password', '')        
    return

def logout(request):
    pass

def my_account(request):
    pass