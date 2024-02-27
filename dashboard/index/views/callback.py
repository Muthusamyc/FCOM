from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.models import BookCallBack
from datetime import datetime
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

@login_required
def listings(request):
    page_no = request.GET.get('page', 1)
    booked_call_backs = BookCallBack.objects.filter(status=0).all().order_by('-id')    
    paginated_booked_call_backs = Paginator(booked_call_backs, 30)
    try:
        list_of_callbackes = paginated_booked_call_backs.page(page_no)
    except PageNotAnInteger:
        list_of_callbackes = paginated_booked_call_backs.page(1)
    except EmptyPage:
        list_of_callbackes = paginated_booked_call_backs.page(paginated_booked_call_backs.num_pages)
    return render(request, 'callback/listings.html', {'booked_call_backs' : list_of_callbackes})

@login_required
def callbacks_update(request, id):
    booked_call_backs = BookCallBack.objects.get(id=id)  
    if request.method == "POST":
        booked_call_backs.status = request.POST.get('status', '')
        booked_call_backs.feedback = request.POST.get('feedback', '')
        booked_call_backs.updated_at = datetime.now()
        booked_call_backs.save()
        
        return redirect(listings)
    return render(request, 'callback/update.html', {'booked_call_backs' : booked_call_backs})

@login_required
def follow_up(request):
    page_no = request.GET.get('page', 1)
    follow_up_calls = BookCallBack.objects.filter(status__gte=1).all().order_by('-id')    
    paginated_follow_up_calls = Paginator(follow_up_calls, 30)
    try:
        list_of_follow_up_calls = paginated_follow_up_calls.page(page_no)
    except PageNotAnInteger:
        list_of_follow_up_calls = paginated_follow_up_calls.page(1)
    except EmptyPage:
        list_of_follow_up_calls = paginated_follow_up_calls.page(paginated_follow_up_calls.num_pages)
    return render(request, 'callback/follow-up.html', {'follow_up_calls' : list_of_follow_up_calls})
