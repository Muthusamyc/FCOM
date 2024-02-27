from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from commons.roles import is_user_superadmin
from home.models import BookCallBack, PartnerForm

from dashboard.services.models import Order, DesingerAssignedOrders

from commons.booking_stages import BookingStage
from commons.user_role import authenticated_user,allowed_users,admin_only

@login_required(login_url="/login/")
@admin_only
def index(request):
    #here we will count all the tables records
    
    if request.user.is_superuser:                   
        book_call_back_count = BookCallBack.objects.filter(status=0).count()
        follow_up_count = BookCallBack.objects.filter(status__gte=1).count()    
        partner_form_count = PartnerForm.objects.count()      
        
        order_booked_count = Order.objects.filter(status=BookingStage.ORDER_BOOKED).count()
        order_assigned_count = Order.objects.filter(status=BookingStage.ORDER_ASSINGED).count()
        order_consulted_count = Order.objects.filter(status=BookingStage.ORDER_CONSULTED).count()
        order_waiting_approval_count = Order.objects.filter(status=BookingStage.WAIT_FOR_APPROVAL).count()
        order_picked_up_count = Order.objects.filter(status=BookingStage.ORDER_PICKEDUP).count()
        order_balance_amount_paid_count = Order.objects.filter(status=BookingStage.BALANCE_AMOUNT_PAID).count()
        order_canceled_count = Order.objects.filter(status=BookingStage.ORDER_CANCELED).count()
        order_failed_count = Order.objects.filter(status=BookingStage.ORDER_FAILED).count()
        order_updated_count = Order.objects.filter(status=BookingStage.ORDER_UPDATED).count()
        order_rejected_count = Order.objects.filter(status=BookingStage.APPROVAL_REJECTED).count()
        order_approved_count = Order.objects.filter(status=BookingStage.APPROVAL_ACCEPTED).count()
        order_in_progress_count = Order.objects.filter(status=BookingStage.ORDER_IN_PROGRESS).count()   
        order_delivered_count = Order.objects.filter(status=BookingStage.ORDER_DELIVERED).count()
        order_intiated_count = Order.objects.filter(status=BookingStage.ORDER_INITIATED).count()
        order_ready_for_dispatch_count = Order.objects.filter(status=BookingStage.READY_FOR_DISPATCH).count()
        order_dispatched_count = Order.objects.filter(status=BookingStage.ORDER_DISPATCHED).count()

        canceled_order_ready_for_dispatch_count = Order.objects.filter(status=BookingStage.ORDER_CANCELED_READY_FOR_DISPATCH).count()
        canceled_order_dispatched_count = Order.objects.filter(status=BookingStage.ORDER_CANCELED_DISPATCHED).count()
        canceled_order_delivered_count = Order.objects.filter(status=BookingStage.ORDER_CANCELED_DELIVERED).count()
        refund_initiated_count = Order.objects.filter(status=BookingStage.REFUND_INITIATED).count()
        refund_completed_count = Order.objects.filter(status=BookingStage.REFUND_COMPLETED).count()
        
        return render(request, "dashboard/index.html", context={
            'book_call_back_count' : book_call_back_count,
            'follow_up_count' : follow_up_count,
            'partner_form_count' : partner_form_count,
            'order_booked_count' : order_booked_count,
            'order_assigned_count' : order_assigned_count,
            'order_consulted_count' : order_consulted_count,
            'order_waiting_approval_count' : order_waiting_approval_count,
            'order_picked_up_count' :order_picked_up_count,
            'order_delivered_count' : order_delivered_count,
            'order_balance_amount_paid_count' : order_balance_amount_paid_count,
            'order_canceled_count' : order_canceled_count,
            'order_failed_count' : order_failed_count,
            'order_updated_count' : order_updated_count,
            'order_approved_count' : order_approved_count,
            'order_intiated_count' : order_intiated_count,
            'order_in_progress_count' : order_in_progress_count,
            'order_delivered_count' : order_delivered_count,
            'order_ready_for_dispatch_count' : order_ready_for_dispatch_count,
            'order_dispatched_count' : order_dispatched_count,
            'canceled_order_dispatch_count' : canceled_order_ready_for_dispatch_count,
            'canceled_order_dispatched_count' : canceled_order_dispatched_count,
            'canceled_order_delivered_count' : canceled_order_delivered_count,
            'refund_initiated_count' : refund_initiated_count,
            'refund_completed_count' : refund_completed_count,
            'order_rejected_count' : order_rejected_count
           
        })
    else:        
        order_booked_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_ASSINGED, designer_id=request.user.id).count()
        order_consulted_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_CONSULTED, designer_id=request.user.id).count()
        order_waiting_approval_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.WAIT_FOR_APPROVAL, designer_id=request.user.id).count()
        order_in_progress_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_IN_PROGRESS, designer_id=request.user.id).count()
        order_canceled_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_CANCELED, designer_id=request.user.id).count()
        order_updated_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_UPDATED, designer_id=request.user.id).count()
        order_picked_up_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_PICKEDUP, designer_id=request.user.id).count()
        order_approved_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.APPROVAL_ACCEPTED, designer_id=request.user.id).count()
        order_rejected_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.APPROVAL_REJECTED, designer_id=request.user.id).count()
        order_delivered_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_DELIVERED, designer_id=request.user.id).count()
        order_balance_amount_paid_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.BALANCE_AMOUNT_PAID, designer_id=request.user.id).count()
        order_ready_for_dispatch_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.READY_FOR_DISPATCH, designer_id=request.user.id).count()
        order_dispatched_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_DISPATCHED, designer_id=request.user.id).count()

        canceled_order_ready_for_dispatch_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_CANCELED_READY_FOR_DISPATCH, designer_id=request.user.id).count()
        canceled_order_dispatched_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_CANCELED_DISPATCHED, designer_id=request.user.id).count()
        canceled_order_delivered_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.ORDER_CANCELED_DELIVERED, designer_id=request.user.id).count()
        refund_initiated_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.REFUND_INITIATED, designer_id=request.user.id).count()
        refund_completed_count = DesingerAssignedOrders.objects.filter(order__status=BookingStage.REFUND_COMPLETED, designer_id=request.user.id).count()
        
        return render(request, "dashboard/index.html", context={           
            'order_booked_count' : order_booked_count,
            'order_consulted_count' : order_consulted_count,
            'order_waiting_approval_count' : order_waiting_approval_count,
            'order_canceled_count' : order_canceled_count,            
            'order_updated_count' : order_updated_count,            
            'order_picked_up_count' : order_picked_up_count,            
            'order_in_progress_count' : order_in_progress_count,
            'order_approved_count' : order_approved_count,
            'order_rejected_count' : order_rejected_count,
            'order_delivered_count' : order_delivered_count,
            'order_balance_amount_paid_count' : order_balance_amount_paid_count,
            'order_ready_for_dispatch_count' : order_ready_for_dispatch_count,
            'order_dispatched_count' : order_dispatched_count,
            'canceled_order_dispatch_count' : canceled_order_ready_for_dispatch_count,
            'canceled_order_dispatched_count' : canceled_order_dispatched_count,
            'canceled_order_delivered_count' : canceled_order_delivered_count,
            'refund_initiated_count' : refund_initiated_count,
            'refund_completed_count' : refund_completed_count,
            'booking_stages' : BookingStage
        })



@login_required
@admin_only
def partners_forms(request):    
    page_no = request.GET.get('page', 1)
    parnters = PartnerForm.objects.all().order_by('-id')    
    paginated_parnters = Paginator(parnters, 30)
    try:
        list_of_parnters = paginated_parnters.page(page_no)
    except PageNotAnInteger:
        list_of_parnters = paginated_parnters.page(1)
    except EmptyPage:
        list_of_parnters = paginated_parnters.page(paginated_parnters.num_pages)
    return render(request, 'partners/listings.html', {'parnters' : list_of_parnters})
