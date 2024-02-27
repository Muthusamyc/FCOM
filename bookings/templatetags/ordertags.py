from commons.booking_stages import STAGES
from django import template
from django.template.defaultfilters import stringfilter
from dashboard.services.models import OrderTracking, TransactionAmount, OrderItems

register = template.Library()

@register.filter
def get_order_status(status):   
    return STAGES[status]

@register.simple_tag
def tracking_date(order_id, status_name ):   
    order_date = OrderTracking.objects.filter(status_name=status_name ,order_id=order_id).last()
    if order_date :
        return order_date.created_on
    else:
        return "Yet-to-Assign"
    
@register.simple_tag
def pickedup_image(order_id):   
    picked_image = OrderItems.objects.filter(order_id=order_id, image__isnull=False).exists()
    if picked_image :
        return True
    else:
        return False

