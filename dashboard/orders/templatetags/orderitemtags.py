from django import template
from dashboard.services.models import OrderTracking, TransactionAmount, Order, StichingItem, CustomerReview
from commons.booking_stages import BOOKING_STAGES_FOR_USER

from datetime import datetime, date, timedelta
import calendar
from dashboard.services.models import Measurementslist 
from django.db.models import Count, Avg, Sum


register = template.Library()

@register.filter
def get_tracking_date(order_id): 
    tracking_date =   OrderTracking.objects.filter(status_name='Approval Pending',order_id=order_id).last()
    return tracking_date.created_on

@register.filter
def get_paid_amount(transaction_id): 
    transactionamt =   TransactionAmount.objects.filter(transaction_id=transaction_id)
    total_amount = 0
    for amount in transactionamt:
        total_amount += float(amount.payment_amount)
    return total_amount

@register.simple_tag
def canceled_after_picked_up(order_id): 
    order_pickedup =   OrderTracking.objects.filter(status_name='Picked Up' ,order_id=order_id).exists()
    return order_pickedup




@register.filter
def get_list_item_report(list, index):
    return list[index]


@register.filter
def designer_assigned_count(designer_assigned):
    today = datetime.today()
    end_date = calendar.monthrange(today.year, today.month)[1]
    designer_assigned = Order.objects.filter(created_on__lte=date(today.year, today.month, end_date), created_on__gte=date(today.year, today.month, 1),designer_assigned__icontains=designer_assigned).count()
    return designer_assigned

@register.filter
def designer_delivered_count(designer_assigned):
    today = datetime.today()
    end_date = calendar.monthrange(today.year, today.month)[1]
    designer_delivered = Order.objects.filter(created_on__lte=date(today.year, today.month, end_date), created_on__gte=date(today.year, today.month, 1),designer_assigned__icontains=designer_assigned,is_order_delivered=1).count()
    return designer_delivered

@register.filter
def designer_completion_percentage(designer_assigned):
    today = datetime.today()
    end_date = calendar.monthrange(today.year, today.month)[1]
    designer_assigned_count = Order.objects.filter(created_on__lte=date(today.year, today.month, end_date), created_on__gte=date(today.year, today.month, 1),designer_assigned__icontains=designer_assigned).count()
    designer_delivered = Order.objects.filter(created_on__lte=date(today.year, today.month, end_date), created_on__gte=date(today.year, today.month, 1),designer_assigned__icontains=designer_assigned,is_order_delivered=1).count()
    if designer_assigned_count == 0:
        percentage = 0
    else:
        percentage = designer_delivered/designer_assigned_count * 100
    return percentage

@register.filter
def get_order_item_name(id):
    item_name = StichingItem.objects.get(id=id)
    return item_name.name


@register.filter
def avg_review(designer_assigned):
    today = datetime.today()
    end_date = calendar.monthrange(today.year, today.month)[1]
    avg_review = CustomerReview.objects.filter(order__created_on__lte=date(today.year, today.month, end_date), order__created_on__gte=date(today.year, today.month, 1),order__is_order_delivered=1, order__designer_assigned__icontains=designer_assigned).aggregate(Avg("rating"))
    return avg_review['rating__avg'] if avg_review['rating__avg'] else 0




@register.simple_tag
def total_order_count(designer_assigned,from_date, to_date):
    if from_date and to_date:
        fromDate = datetime.strptime(from_date, '%Y-%m-%d')
        date_obj = datetime.strptime(to_date, '%Y-%m-%d')
        toDate =  date_obj + timedelta(days=1)
        order_count = Order.objects.filter(created_on__lte=date(toDate.year, toDate.month, toDate.day), created_on__gte=date(fromDate.year, fromDate.month, fromDate.day), designer_assigned__icontains=designer_assigned).count()
    else:
        today = datetime.today()
        end_date = calendar.monthrange(today.year, today.month)[1]
        order_count = Order.objects.filter(created_on__lte=date(today.year, today.month, end_date), created_on__gte=date(today.year, today.month, 1), designer_assigned__icontains=designer_assigned).count()
    return order_count


@register.simple_tag
def completed_order_count(designer_assigned,from_date, to_date):
    if from_date and to_date:
        fromDate = datetime.strptime(from_date, '%Y-%m-%d')
        date_obj = datetime.strptime(to_date, '%Y-%m-%d')
        toDate =  date_obj + timedelta(days=1)
        order_count = Order.objects.filter(created_on__lte=date(toDate.year, toDate.month, toDate.day), created_on__gte=date(fromDate.year, fromDate.month, fromDate.day),is_order_delivered=1, designer_assigned__icontains=designer_assigned).count()
    else:
        today = datetime.today()
        end_date = calendar.monthrange(today.year, today.month)[1]
        order_count = Order.objects.filter(created_on__lte=date(today.year, today.month, end_date), created_on__gte=date(today.year, today.month, 1),is_order_delivered=1, designer_assigned__icontains=designer_assigned).count()
    return order_count

@register.simple_tag
def picked_order_count(designer_assigned,from_date, to_date):
    if from_date and to_date:
        fromDate = datetime.strptime(from_date, '%Y-%m-%d')
        date_obj = datetime.strptime(to_date, '%Y-%m-%d')
        toDate =  date_obj + timedelta(days=1)
        order_count = Order.objects.filter(created_on__lte=date(toDate.year, toDate.month, toDate.day), created_on__gte=date(fromDate.year, fromDate.month, fromDate.day),pickup_date__isnull=False, designer_assigned__icontains=designer_assigned).count()
    else:
        today = datetime.today()
        end_date = calendar.monthrange(today.year, today.month)[1]
        order_count = Order.objects.filter(created_on__lte=date(today.year, today.month, end_date), created_on__gte=date(today.year, today.month, 1), pickup_date__isnull=False, designer_assigned__icontains=designer_assigned).count()
    return order_count



@register.simple_tag
def ordertracking_date(order_id, status_name):
    try:
        order =   OrderTracking.objects.get(status_name=status_name,order_id=order_id)
        order_pickedup = order.created_on
    except:
       order_pickedup = 'Not yet Assigned'
    print(order_pickedup)
    return order_pickedup


@register.simple_tag
def ordertracking_date(order_id, status_name):
    try:
        tracking_date =   OrderTracking.objects.get(status_name=status_name,order_id=order_id)
        order_date = tracking_date.created_on
    except:
       order_date = 'Not yet Assigned'
    return order_date


@register.simple_tag
def no_of_days(order_id, status_name):
    try:
        order = Order.objects.get(id=order_id)
        order_created_date = order.created_on
        tracking_date =   OrderTracking.objects.get(status_name=status_name,order_id=order_id)
        order_date = tracking_date.created_on
        diff = order_date - order_created_date
        no_of_days = diff.days
    except:
       no_of_days = 'yet to Complete'
    return no_of_days


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='percentage')
def percentage(value, arg):
    if value :
        result =  arg/value * 100
    else:
        result =0
    return result




@register.filter
def sum_values(queryset, field_name):
    return queryset.aggregate(sum_total=Sum(field_name))['sum_total']
