class BookingStage:
    ORDER_BOOKED = 1
    ORDER_UPDATED = 2
    APPROVAL_ACCEPTED = 3
    APPROVAL_REJECTED = 4
    ESTIMATED_PAYMENT = 5
    ESTIMATED_PAYMENT_PAID = 6
    ORDER_IN_PROGRESS = 7
    ORDER_SHIPPED = 8
    ORDER_DELIVERED = 9
    ORDER_CANCELED = 10
    REFUND_INITIATED = 11
    REFUND_PENDING = 12
    REFUND_COMPLETED = 13

STAGES = (
    (BookingStage.ORDER_BOOKED, "Order Booked")
)

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def get_order_status(status):
    return STAGES[status]


