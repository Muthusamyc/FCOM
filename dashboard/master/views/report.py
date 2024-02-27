from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import calendar


from dashboard.services.models import  OrderTracking, TransactionDetails, Order, OrderItems, StichingItemRelation, CustomerReview, StichingCategory
from home.models import BookCallBack
from commons.user_role import authenticated_user,allowed_users,admin_only
from dashboard.master.models import User
from commons.roles import DESIGNER
from django.db.models import Sum
from datetime import datetime, date, timedelta
from django.db.models import Count, Avg
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q




@login_required
@admin_only
def customer_report(request):
    users = User.objects.filter(role=3).all()
    if request.method == 'POST':
        fromDate = request.POST.get('fromDate','')
        toDate = request.POST.get('toDate','')
        fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
        date_obj = datetime.strptime(toDate, '%Y-%m-%d')
        toDate =  date_obj + timedelta(days=1)
        users = User.objects.filter(date_joined__lte=date(toDate.year, toDate.month, toDate.day), date_joined__gte=date(fromDate.year, fromDate.month, fromDate.day), role=3).all()
        return render(request, 'report/customer_report.html', {'users':users})

    return render(request, 'report/customer_report.html', {'users':users})


@login_required
@admin_only
def designer_sales(request):
    designers = User.objects.filter(role=2).all()
    transactiondetails = TransactionDetails.objects.filter(order__designer_assigned__isnull=False).exclude(Q(order__status=15) | Q(order__status=0) | Q(order__is_order_cancaled=1)).all()
    net_amount_value = transactiondetails.aggregate(Sum('net_amount'))['net_amount__sum']
    balance_amt_due_value = transactiondetails.aggregate(Sum('balance_amt_due'))['balance_amt_due__sum']
    paid_amt_value = (net_amount_value if net_amount_value else 0 )- (balance_amt_due_value if balance_amt_due_value else 0)
    if request.method == 'POST':
        designer = request.POST.get('designer','')
        fromDate = request.POST.get('fromDate','')
        toDate = request.POST.get('toDate','')
        fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
        date_obj = datetime.strptime(toDate, '%Y-%m-%d')
        toDate =  date_obj + timedelta(days=1)
        if designer:
            transactiondetails = TransactionDetails.objects.filter(order__designer_assigned=designer, order__created_on__lte=date(toDate.year, toDate.month, toDate.day), order__created_on__gte=date(fromDate.year, fromDate.month, fromDate.day),order__designer_assigned__isnull=False).exclude(Q(order__status=15) | Q(order__status=0) | Q(order__is_order_cancaled=1)).all()
        else: 
            transactiondetails = TransactionDetails.objects.filter(order__created_on__lte=date(toDate.year, toDate.month, toDate.day), order__created_on__gte=date(fromDate.year, fromDate.month, fromDate.day),order__designer_assigned__isnull=False).exclude(Q(order__status=15) | Q(order__status=0) | Q(order__is_order_cancaled=1)).all()
        net_amount_value = transactiondetails.aggregate(Sum('net_amount'))['net_amount__sum']
        balance_amt_due_value = transactiondetails.aggregate(Sum('balance_amt_due'))['balance_amt_due__sum']
        paid_amt_value = (net_amount_value if net_amount_value else 0 )- (balance_amt_due_value if balance_amt_due_value else 0)
        return render(request, 'report/designer_sales.html', {'transactiondetails': transactiondetails,'designers': designers,
                                                          'net_amount_value':net_amount_value,'balance_amt_due_value':balance_amt_due_value,
                                                          'paid_amt_value':paid_amt_value})

    return render(request, 'report/designer_sales.html', {'transactiondetails': transactiondetails,'designers': designers,
                                                          'net_amount_value':net_amount_value,'balance_amt_due_value':balance_amt_due_value,
                                                          'paid_amt_value':paid_amt_value})


@login_required
@admin_only
def amount_collected(request):
    transactiondetails = TransactionDetails.objects.exclude(Q(order__status=15) | Q(order__status=0) | Q(order__is_order_cancaled=1)).all()
    net_amount_value = transactiondetails.aggregate(Sum('net_amount'))['net_amount__sum']
    sub_total_value = transactiondetails.aggregate(Sum('sub_total'))['sub_total__sum']
    balance_amt_due_value = transactiondetails.aggregate(Sum('balance_amt_due'))['balance_amt_due__sum']
    paid_amt_value = (net_amount_value if net_amount_value else 0 )- (balance_amt_due_value if balance_amt_due_value else 0)
    if request.method == 'POST':
        fromDate = request.POST.get('fromDate','')
        toDate = request.POST.get('toDate','')
        fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
        date_obj = datetime.strptime(toDate, '%Y-%m-%d')
        toDate =  date_obj + timedelta(days=1)
        transactiondetails = TransactionDetails.objects.filter(order__created_on__lte=date(toDate.year, toDate.month, toDate.day), order__created_on__gte=date(fromDate.year, fromDate.month, fromDate.day)).exclude(Q(order__status=15) | Q(order__status=0) | Q(order__is_order_cancaled=1)).all()
        net_amount_value = transactiondetails.aggregate(Sum('net_amount'))['net_amount__sum']
        sub_total_value = transactiondetails.aggregate(Sum('sub_total'))['sub_total__sum']
        balance_amt_due_value = transactiondetails.aggregate(Sum('balance_amt_due'))['balance_amt_due__sum']
        paid_amt_value = (net_amount_value if net_amount_value else 0 )- (balance_amt_due_value if balance_amt_due_value else 0)
        return render(request, 'report/amount_collected.html',{'transactiondetails':transactiondetails,
                                                           'net_amount_value':net_amount_value,'sub_total_value':sub_total_value,
                                                           'balance_amt_due_value':balance_amt_due_value,'paid_amt_value':paid_amt_value})

    return render(request, 'report/amount_collected.html',{'transactiondetails':transactiondetails,
                                                           'net_amount_value':net_amount_value,'sub_total_value':sub_total_value,
                                                           'balance_amt_due_value':balance_amt_due_value,'paid_amt_value':paid_amt_value})




@login_required
@admin_only
def top_sales(request):
    top_sales_men = {}
    top_sales_women = {}
    top_sales_home_decor = {}
    top_sales_kids = {}

    men = StichingCategory.objects.get(name='Men')
    women = StichingCategory.objects.get(name='Women')
    home_decor = StichingCategory.objects.get(name='Home Decor')
    kid = StichingCategory.objects.get(name='Kids')
    mens = StichingItemRelation.objects.filter(category_id=men.id).all()
    womens = StichingItemRelation.objects.filter(category_id=women.id).all()
    home_decors = StichingItemRelation.objects.filter(category_id=home_decor.id).all()
    kids = StichingItemRelation.objects.filter(category_id=kid.id).all()
    
    if list(i.id for i in mens):
        top_sales_men = OrderItems.objects.filter(product_item_id__in=list(men.id for men in mens)).all().values('product_item_id').annotate(total=Count('qty')).order_by('-total')[:10]
    if list(i.id for i in womens):
        top_sales_women = OrderItems.objects.filter(product_item_id__in=list(i.id for i in womens)).values('product_item_id').annotate(total=Count('qty')).order_by('-total')[:10]
    if list(i.id for i in home_decors):
        top_sales_home_decor = OrderItems.objects.filter(product_item_id__in=list(i.id for i in home_decors)).values('product_item_id').annotate(total=Count('qty')).order_by('-total')[:10]
    if list(i.id for i in kids):
        top_sales_kids = OrderItems.objects.filter(product_item_id__in=list(i.id for i in kids)).values('product_item_id').annotate(total=Count('qty')).order_by('-total')[:10]
    
    return render(request, 'report/top_sales.html', {'top_sales_men': top_sales_men, 'top_sales_women': top_sales_women, 
                                                     'top_sales_home_decor':top_sales_home_decor, 'top_sales_kids':top_sales_kids })


@login_required
@admin_only
def designer_performance(request): 
    designers = User.objects.filter(role=DESIGNER).all()
    fromDate = ''
    toDate = ''
    if request.method == 'POST':
        fromDate = request.POST.get('fromDate','')
        toDate = request.POST.get('toDate','')
        return render(request, 'report/designer_performance.html', {'designers': designers,'fromDate':fromDate, 'toDate':toDate})
    return render(request, 'report/designer_performance.html', {'designers': designers,'fromDate':fromDate, 'toDate':toDate})

@login_required
@admin_only
def designer_reviews(request): 
    reviews = CustomerReview.objects.all()
    if request.method == 'POST':
        fromDate = request.POST.get('fromDate','')
        toDate = request.POST.get('toDate','')
        fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
        date_obj = datetime.strptime(toDate, '%Y-%m-%d')
        toDate =  date_obj + timedelta(days=1)
        reviews = CustomerReview.objects.filter(created_on__lte=date(toDate.year, toDate.month, toDate.day), created_on__gte=date(fromDate.year, fromDate.month, fromDate.day)).all()
    return render(request, 'report/designer_reviews.html', {'reviews':reviews})




@login_required
@admin_only
def order_report(request):
    orders = Order.objects.exclude(Q(status=15) | Q(status=0) | Q(is_order_cancaled=1)).all()
    if request.method == 'POST':
        fromDate = request.POST.get('fromDate','')
        toDate = request.POST.get('toDate','')
        fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
        date_obj = datetime.strptime(toDate, '%Y-%m-%d')
        toDate =  date_obj + timedelta(days=1)
        orders = Order.objects.filter(created_on__lte=date(toDate.year, toDate.month, toDate.day), created_on__gte=date(fromDate.year, fromDate.month, fromDate.day)).exclude(status=15).all()
        return render(request, 'report/order_report.html',{'orders':orders})

    return render(request, 'report/order_report.html',{'orders':orders})



@login_required
@admin_only
def report_orders_listing(request, status):
    today = datetime.today()
    page_no = request.GET.get('page', 1)
    end_date = calendar.monthrange(today.year, today.month)[1]
    orders_query = Order.objects.filter(ordertracking__status_name=status, ordertracking__created_on__lte=date(today.year, today.month, end_date), ordertracking__created_on__gte=date(today.year, today.month, 1))

    paginated_orders = Paginator(orders_query, 30)
    try:
        list_of_orders = paginated_orders.page(page_no)
    except PageNotAnInteger:
        list_of_orders = paginated_orders.page(1)
    except EmptyPage:
        list_of_orders = paginated_orders.page(paginated_orders.num_pages)
    

    return render(request, "orders/assigned_orders.html", {"orders": list_of_orders})


@login_required
@admin_only
def order_movement_report(request):
     orders = Order.objects.filter(is_order_delivered=1).exclude(Q(status=15) | Q(status=0) | Q(is_order_cancaled=1)).all()
     if request.method == 'POST':
        fromDate = request.POST.get('fromDate','')
        toDate = request.POST.get('toDate','')
        fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
        date_obj = datetime.strptime(toDate, '%Y-%m-%d')
        toDate =  date_obj + timedelta(days=1)
        orders = Order.objects.filter(created_on__lte=date(toDate.year, toDate.month, toDate.day), created_on__gte=date(fromDate.year, fromDate.month, fromDate.day),is_order_delivered=1).exclude(Q(status=15) | Q(status=0) | Q(is_order_cancaled=1)).all()
        return render(request, "report/order_movement.html", {'orders': orders})
     return render(request, "report/order_movement.html", {'orders': orders})
