
from commons.booking_stages import BookingStage
from dashboard.services.models import Order


def update_order_status(order_id, status):    
    #update order 
    order = Order.objects.get(id=order_id)
    order.is_order_updated_by_designer = True
    order.status = status
    order.save()
    return True
    