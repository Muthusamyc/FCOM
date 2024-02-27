from commons.booking_stages import STAGES
from django import template
from django.template.defaultfilters import stringfilter

from commons.services import SERVICE_ITEM_TYPE

register = template.Library()

@register.filter
def get_order_status(status):   
    return STAGES[status]

@register.filter
def get_item_type(item_type_id):
    return SERVICE_ITEM_TYPE[item_type_id]