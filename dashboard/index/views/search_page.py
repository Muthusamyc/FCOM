from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dashboard.master.models import User
from dashboard.services.models import Order
from django.db.models import Q

@login_required
def search_order(request):
    if request.method == 'POST':
        search_opt = request.POST.get('search','').strip()
        filter_opt = request.POST.get('filter','').strip()
        if filter_opt == "first_name":
            orders = Order.objects.all().filter(made_by__first_name__icontains=search_opt).exclude(Q(status=15) | Q(status=0)).order_by("-id")
        elif filter_opt == "mobile_no":
            orders = Order.objects.all().filter(made_by__mobile_no=search_opt).exclude(Q(status=15) | Q(status=0)).order_by("-id")
        else:
            orders = Order.objects.all().filter(id=int(search_opt)).exclude(Q(status=15) | Q(status=0)).order_by("-id")
        return render(request, 'search_page.html', {'orders':orders, 'search_opt':search_opt, 'filter_opt':filter_opt})
    return render(request, 'search_page.html')

