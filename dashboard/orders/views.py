import threading
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.utils import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.forms.models import model_to_dict

from bookings.api.order import (calculate_net_amount, calculate_taxes, calculate_state_and_central_tax)
from commons.booking_stages import STAGES, BookingStage
from commons.mail.email_config import (send_consultation_msg,
                                       send_order_dispatched_msg,
                                       send_order_ready_for_dispatch_msg,
                                       send_order_waiting_for_approval_msg)
from commons.sms_templates import *
from commons.roles import DESIGNER
from commons.services import STICHING_SERVICES
from commons.user_role import (DESIGNER, admin_only, )
from dashboard.master.models import User
from dashboard.services.models import (DesingerAssignedOrders, ItemsInCart,
                                       Order, OrderItems, OrderTracking,
                                       PayTMTransactionDetails, StichingItem,
                                       StichingItemRelation, CustomerReview,
                                       TransactionDetails, Measurement, Measurementslist, MeasurementGroups)

from .helpers import update_order_status

ORDER_LISTING_PAGES = {
  #  BookingStage.ORDER_BOOKED : 'orders_listing.html',
    BookingStage.ORDER_ASSINGED : 'orders/assigned_orders.html',
    BookingStage.ORDER_CONSULTED : 'orders/visit_and_consultation.html',
    BookingStage.ORDER_IN_PROGRESS : 'orders/in_progress.html',
    BookingStage.WAIT_FOR_APPROVAL : 'orders/approval_pending.html',
    BookingStage.ORDER_CONSULTED : 'orders/visit_and_consultation.html',
    BookingStage.ORDER_IN_PROGRESS : 'orders/in_progress.html',
    BookingStage.WAIT_FOR_APPROVAL : 'orders/approval_pending.html',
    
}


@login_required
@admin_only
def orders_listing(request, id):
    page_no = request.GET.get('page', 1)
    orders_query = Order.objects.all().filter(status=id).order_by("-id")
    paginated_orders = Paginator(orders_query, 30)
    try:
        list_of_orders = paginated_orders.page(page_no)
    except PageNotAnInteger:
        list_of_orders = paginated_orders.page(1)
    except EmptyPage:
        list_of_orders = paginated_orders.page(paginated_orders.num_pages)
    
    order_status_name = STAGES[id]
    template_page_name = ORDER_LISTING_PAGES[id] if id in ORDER_LISTING_PAGES else "orders_listing.html"
    page_context = {"orders": list_of_orders,  'order_status_name' : order_status_name}
    return render(request, template_page_name, page_context)
    

@login_required
def order_listing_for_designer(request, order_status):
    orders_query_list = DesingerAssignedOrders.objects.filter(
        designer_id=request.user.id, order__status=order_status).order_by('-id').all()
    
    order_status_name = STAGES[order_status]
    
    page_context = {'designer_orders': orders_query_list, 'DESIGNER': DESIGNER, 'order_status_name' : order_status_name}
    template_page_name = ORDER_LISTING_PAGES[order_status] if order_status in ORDER_LISTING_PAGES else "orders_listing.html"
    return render(request, template_page_name, page_context)
   

@login_required
@admin_only
def order_details(request, id):
    groups = MeasurementGroups.objects.all()
    order = Order.objects.get(id=id)
    
    measurements = Measurement.objects.filter(user_id=order.made_by.id, is_master=1).all()
    
  
    paytm_transaction_details = {}
    if order.status != BookingStage.ORDER_INITIATED:
        paytm_transaction_details = PayTMTransactionDetails.objects.filter(
            order_id=order.id).all()

  #  cart_detail = order.cart
    order_items = OrderItems.objects.filter(order_id=order.id).all()
    transaction_details = TransactionDetails.objects.filter(
        order_id=order.id).last()
    try:
        reviews = CustomerReview.objects.get(order_id= order.id)
    except:
        reviews = {}

    all_services = {}
    for service_name, service_obj in STICHING_SERVICES.items():
        all_services[service_name] = service_obj.objects.all().values(
            'id', 'name')

    designers = User.objects.filter(role=DESIGNER).all()

    order_tracking_details = OrderTracking.objects.filter(order_id=id, status__in=[BookingStage.ORDER_BOOKED, BookingStage.APPROVAL_ACCEPTED,
                                                                                   BookingStage.ORDER_UPDATED, BookingStage.ORDER_PICKEDUP, BookingStage.ORDER_IN_PROGRESS, BookingStage.ORDER_DELIVERED]).all()

    if request.method == "POST":
        transaction_amount = transaction_details.taxable_order_amount - \
            (transaction_details.extra_material + transaction_details.designer_charges +
             transaction_details.shipping_charges - transaction_details.coupon_discount)
        extra_material = float(request.POST.get('extra_material', '') if request.POST.get(
            'extra_material', '') else transaction_details.extra_material)
        desginer_charges = float(request.POST.get('designer_charges', '') if request.POST.get(
            'designer_charges', '') else transaction_details.designer_charges)
        coupon_discount = float(request.POST.get('coupon_discount', '') if request.POST.get(
            'coupon_discount', '') else transaction_details.coupon_discount)
        shipping_charges = float(request.POST.get('shipping_charges', '') if request.POST.get(
            'shipping_charges', '') else transaction_details.shipping_charges)
        transaction_details.extra_material = extra_material
        transaction_details.designer_charges = desginer_charges
        transaction_details.coupon_discount = coupon_discount
        transaction_details.shipping_charges = shipping_charges
        total_amount_without_tax = (
            transaction_amount + extra_material + shipping_charges + desginer_charges) - coupon_discount

        transaction_details.taxable_order_amount = total_amount_without_tax
        tax_charges = calculate_taxes(total_amount_without_tax)
        net_amount = total_amount_without_tax + tax_charges

        transaction_details.calcualted_tax = tax_charges
        transaction_details.cgst_tax_charges = calculate_state_and_central_tax(total_amount_without_tax)
        transaction_details.igst_tax_charges = calculate_state_and_central_tax(total_amount_without_tax)

        transaction_details.net_amount = net_amount
        transaction_details.balance_amt_due = net_amount - \
            (transaction_details.estimation_paid_amount +
             transaction_details.advance_paid_amount)

        transaction_details.save()
        return redirect(order_details, id)
    return render(request, 'order_details.html', {
        'order': order,
        'paytm_transactions': paytm_transaction_details,
        'transaction_details': transaction_details,
        # 'cart' : cart_detail,
        'items': order_items,
        'services': all_services,
        'designers': designers,
        'tracking_details': order_tracking_details,
        'measurements' : measurements,
        'groups' : groups,
        'reviews' : reviews,
        

    })


@login_required
@admin_only
def add_extra_material_to_order(request):

    if request.method == "POST":
        extra_material = request.POST.get('extra_material', '')
        order_id = request.POST.get('orderId')

        update_related_transaction = TransactionDetails.objects.get(
            order_id=order_id)
        previous_extra_material = update_related_transaction.extra_material
        update_related_transaction.extra_material = extra_material
        update_related_transaction.taxable_order_amount = (
            update_related_transaction.taxable_order_amount - previous_extra_material) + float(extra_material)
        tax_charges = calculate_taxes(
            update_related_transaction.taxable_order_amount)
        total_amt_with_extra_fabric = update_related_transaction.sub_total + \
            float(extra_material)
        net_amount = calculate_net_amount(total_amt_with_extra_fabric, tax_charges,
                                          update_related_transaction.shipping_charges, update_related_transaction.designer_charges)

        update_related_transaction.calcualted_tax = tax_charges
        update_related_transaction.cgst_tax_charges = calculate_state_and_central_tax(update_related_transaction.taxable_order_amount)
        update_related_transaction.igst_tax_charges = calculate_state_and_central_tax(update_related_transaction.taxable_order_amount)


        update_related_transaction.net_amount = net_amount
        update_related_transaction.balance_amt_due = net_amount - \
            (update_related_transaction.estimation_paid_amount +
             update_related_transaction.advance_paid_amount)
        update_related_transaction.save()
        update_order_status(order_id, BookingStage.ORDER_CONSULTED)
    return redirect(order_details, order_id)

# disgarded for now
@login_required
@admin_only
def add_item_to_order(request):

    if request.method == "POST":
        designer_updated_price = request.POST.get('designer_updated_price', '')
        item_id = request.POST.get('item', '')
        qty = request.POST.get('qty', '')
        order_id = request.POST.get('orderId')
        cart_id = request.POST.get('cartId')

        sub_total_after_adding_this_item = float(
            designer_updated_price) * int(qty)

        new_item_in_cart = ItemsInCart()
        new_item_in_cart.cart_id = cart_id
        new_item_in_cart.item_id = item_id
        new_item_in_cart.designer_updated_price = designer_updated_price
        new_item_in_cart.is_cart_item_updated = True
        new_item_in_cart.sub_total = sub_total_after_adding_this_item
        new_item_in_cart.qty = qty
        new_item_in_cart.save()

        update_related_transaction = TransactionDetails.objects.get(
            order_id=order_id)

        new_sub_total = update_related_transaction.sub_total + \
            sub_total_after_adding_this_item

        update_related_transaction.sub_total = new_sub_total
        tax_charges = calculate_taxes(new_sub_total)
        net_amount = calculate_net_amount(
            new_sub_total, tax_charges, update_related_transaction.shipping_charges, update_related_transaction.designer_charges)

        update_related_transaction.net_amount = net_amount

        update_related_transaction.calcualted_tax = tax_charges
        update_related_transaction.cgst_tax_charges = calculate_state_and_central_tax(new_sub_total)
        update_related_transaction.igst_tax_charges = calculate_state_and_central_tax(new_sub_total)
        update_related_transaction.balance_amt_due = net_amount - \
            (update_related_transaction.estimation_paid_amount +
             update_related_transaction.advance_paid_amount)
        update_related_transaction.save()

        order = Order.objects.get(id=order_id)
        order.is_order_updated_by_designer = True
        order.save()

    return redirect(order_details, order_id)

@login_required
@admin_only
def update_order_item_price_by_designer(request):
    if request.method == "POST":
        order_id = request.POST.get('orderId')
        cart_id = request.POST.get('cartId')
        item_id = request.POST.get('itemId')
        new_item_price_by_designer = request.POST.get('itemUpdatedPrice')
        item_to_be_updated = OrderItems.objects.get(id=item_id)
        old_sub_total = item_to_be_updated.sub_total

        item_to_be_updated.designer_updated_price = new_item_price_by_designer
        item_to_be_updated.is_cart_item_updated = True
        item_to_be_updated.sub_total = float(
            new_item_price_by_designer) * item_to_be_updated.qty
        item_to_be_updated.save()

        update_related_transaction = TransactionDetails.objects.get(
            order_id=order_id)

        # now once the item is updated formula (subtotal - old_sub_total) + updated_item_price
        new_sub_total = (update_related_transaction.sub_total -
                         old_sub_total) + item_to_be_updated.sub_total
        update_related_transaction.sub_total = new_sub_total

        taxable_amount = new_sub_total + update_related_transaction.designer_charges + \
            update_related_transaction.shipping_charges + \
            update_related_transaction.extra_material
        tax_charges = calculate_taxes(taxable_amount)
        net_amount = taxable_amount + tax_charges

        update_related_transaction.net_amount = net_amount

        update_related_transaction.calcualted_tax = tax_charges
        update_related_transaction.cgst_tax_charges = calculate_state_and_central_tax(taxable_amount)
        update_related_transaction.igst_tax_charges = calculate_state_and_central_tax(taxable_amount)

        update_related_transaction.taxable_order_amount = taxable_amount
        update_related_transaction.balance_amt_due = net_amount - \
            (update_related_transaction.estimation_paid_amount +
             update_related_transaction.advance_paid_amount)
        update_related_transaction.save()

        # update order
        # update_order_status(order_id, BookingStage.ORDER_PICKEDUP)
        # order = Order.objects.get(id=order_id)
        # order.is_order_updated_by_designer = True
        # order.status = BookingStage.ORDER_UPDATED
        # order.save()

        return redirect(order_details, order_id)

@login_required
@admin_only
def update_delivery_date(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderId', '')        
        order = Order.objects.get(id=order_id)
        order.status = BookingStage.ORDER_DELIVERED
        order.save()
        new_order_tracker_entry = OrderTracking()
        new_order_tracker_entry.status = BookingStage.ORDER_DELIVERED
        new_order_tracker_entry.status_name = STAGES[BookingStage.ORDER_DELIVERED]
        new_order_tracker_entry.created_on = datetime.now()
        new_order_tracker_entry.order_id = order_id
        new_order_tracker_entry.save()
        return redirect(order_details, order_id)

@login_required
@admin_only
def assign_order_designer(request):
    if request.method == "POST":
        designer_id = request.POST.get('designer', '')
        order_id = request.POST.get('orderId', '')
        try:
            order = Order.objects.get(id=order_id)
            order.status = BookingStage.ORDER_ASSINGED
            order.save()

            order_tracker = OrderTracking.objects.filter(
                order_id=order_id, status=BookingStage.ORDER_ASSINGED).last()

            if order_tracker:
                order_tracker.update_on = datetime.now()
                order_tracker.save()
            else:
                new_order_tracker_entry = OrderTracking()
                new_order_tracker_entry.status = BookingStage.ORDER_ASSINGED
                new_order_tracker_entry.status_name = STAGES[BookingStage.ORDER_ASSINGED]
                new_order_tracker_entry.created_on = datetime.now()
                new_order_tracker_entry.order_id = order_id
                new_order_tracker_entry.save()

            assigned_designer = DesingerAssignedOrders.objects.filter(order_id=order_id).exists()
            if assigned_designer:
                assigned_designer = DesingerAssignedOrders.objects.get(order_id=order_id)
                assigned_designer.designer_id = designer_id
                assigned_designer.assinged_on = datetime.now()
                assigned_designer.user_id = order.made_by.id
                assigned_designer.save()
            else:
                assinge_to_designer = DesingerAssignedOrders()
                assinge_to_designer.order_id = order_id
                assinge_to_designer.designer_id = designer_id
                assinge_to_designer.assinged_on = datetime.now()
                assinge_to_designer.status = 1
                assinge_to_designer.save()
        except IntegrityError as e:
            messages.add_message(request, messages.INFO, "Order is Assigned")
            return redirect(orders_listing, BookingStage.ORDER_BOOKED)

        user = User.objects.get(id=designer_id)
        order = Order.objects.get(id=order_id)
        order.designer_assigned = user.first_name + " " + user.last_name
        order.save()
        return redirect(orders_listing, BookingStage.ORDER_BOOKED)

@login_required
@admin_only
def update_order_service_date_for_order(request, id):
    if request.method == "POST":
        if request.user.is_superuser:
            redirect_function = orders_listing
        elif request.user.role == DESIGNER:
            redirect_function = order_listing_for_designer
        consultation_date = request.POST.get('consultation_date', '')
        inprogress_date = request.POST.get('inprogress_date', '')     
        delivery_date = request.POST.get('delivery_date', '')
        dispatch = request.POST.get('dispatch', '')
        dispatched = request.POST.get('dispatched', '')
        order_id = id
        order = Order.objects.get(id=order_id)

        mailto = order.made_by.email
        customer_name = order.made_by.first_name + " " + order.made_by.last_name
        mobile_no = order.made_by.mobile_no
        
        
        ORDER_STATUS = None
        # if date_type == "Pick Up":
        #     order.pickup_date = date
        #     ORDER_STATUS = BookingStage.ORDER_PICKEDUP
        if dispatched:
            delivery_date = datetime.strptime(delivery_date, '%d-%m-%Y')
            order.delivery_date = delivery_date
            ORDER_STATUS = BookingStage.ORDER_DISPATCHED
            dispatched_sms(mobile_no, order_id)
            if mailto:
                tread = threading.Thread(target=send_order_dispatched_msg, args=[customer_name, order_id, mailto])
                tread.start()
        elif dispatch:
            delivery_date = datetime.strptime(delivery_date, '%d-%m-%Y')
            order.delivery_date = delivery_date
            ORDER_STATUS = BookingStage.READY_FOR_DISPATCH  
            dispatch_status(mobile_no, order_id)
            if mailto:
                tread = threading.Thread(target=send_order_ready_for_dispatch_msg, args=[customer_name, delivery_date.strftime("%b %d %Y"), order_id, mailto])
                tread.start()

        elif consultation_date:
            consultation_date = datetime.strptime(consultation_date, '%d-%m-%Y')
            order.consultation_date = consultation_date       
            ORDER_STATUS = BookingStage.ORDER_CONSULTED
            if order.service_type.name == "Home Visit":
                visit_consult_sms(mobile_no, consultation_date.strftime("%b %d %Y"))
                if mailto:
                    tread = threading.Thread(target=send_consultation_msg, args=[customer_name, consultation_date.strftime("%b %d %Y") , mailto])
                    tread.start()
        elif inprogress_date or delivery_date:
            if not inprogress_date:
                delivery_date = datetime.strptime(delivery_date, '%d-%m-%Y')
                order.delivery_date = delivery_date
                ORDER_STATUS = BookingStage.ORDER_IN_PROGRESS
            else:
                inprogress_date = datetime.strptime(inprogress_date, '%d-%m-%Y')
                delivery_date = datetime.strptime(delivery_date, '%d-%m-%Y')
                order.inprogress_date = inprogress_date
                order.delivery_date = delivery_date
                ORDER_STATUS = BookingStage.ORDER_IN_PROGRESS
        
            
            
        order.save()
        update_order_status(order_id, ORDER_STATUS)
        
        order_tracker = OrderTracking.objects.filter(
                order_id=order_id, status=ORDER_STATUS).last()

        if order_tracker:
            order_tracker.created_on = datetime.now()
            order_tracker.save()
        else:
            new_order_tracker_entry = OrderTracking()
            new_order_tracker_entry.status = ORDER_STATUS
            new_order_tracker_entry.status_name = STAGES[ORDER_STATUS]
            new_order_tracker_entry.created_on = datetime.now()
            new_order_tracker_entry.order_id = order_id
            new_order_tracker_entry.save()
      
        return redirect(redirect_function, order.status)

@login_required
@admin_only
def update_order_status_by_deisnger(request):
    if request.method == "POST":
        order_id = request.POST.get('orderId', '')
        status_type = request.POST.get('statusType', '')

        check_tracker = OrderTracking.objects.filter(
            status=status_type, order_id=order_id).exists()
        if check_tracker:
            update_tracker = OrderTracking.objects.filter(
                status=status_type, order_id=order_id).last()
            update_tracker.created_on = datetime.now()
            update_tracker.save()
        else:
            order_tracker = OrderTracking()
            order_tracker.order_id = order_id
            order_tracker.status = status_type
            order_tracker.created_on = datetime.now()
            order_tracker.status_name = STAGES[int(status_type)]
            order_tracker.save()

        update_order_status(order_id, status_type)
        return redirect(order_details, order_id)

@login_required
@admin_only
def send_approval_request(request):
    if request.method == 'POST':
        order_id = request.POST.get('id', '')   
        order = Order.objects.get(id=order_id)
        mailto = order.made_by.email
        customer_name = order.made_by.first_name + " " + order.made_by.last_name
        mobile_no = order.made_by.mobile_no
        
        order.status = BookingStage.WAIT_FOR_APPROVAL
        order.save()

        new_order_tracker_entry = OrderTracking()
        new_order_tracker_entry.status = BookingStage.WAIT_FOR_APPROVAL
        new_order_tracker_entry.status_name = STAGES[BookingStage.WAIT_FOR_APPROVAL]
        new_order_tracker_entry.order_id = order_id
        new_order_tracker_entry.save()

        mailto = order.made_by.email
        waiting_for_approval_sms(mobile_no, order_id)
        if mailto:
            tread = threading.Thread(target=send_order_waiting_for_approval_msg, args=[customer_name, order_id, mailto])
            tread.start()
        return JsonResponse({"status":1})
    
@login_required
@admin_only
def order_pickedup(request):
    if request.method == 'POST':
        picked = request.POST.getlist('picked')
        for order_id in picked:
            order = Order.objects.get(id=order_id)


            order.pickup_date = datetime.now()
            order.save()
            ORDER_STATUS = BookingStage.ORDER_PICKEDUP
            update_order_status(order_id, ORDER_STATUS)
            
            order_tracker = OrderTracking.objects.filter(
                    order_id=order_id, status=ORDER_STATUS).last()

            if order_tracker:
                order_tracker.created_on = datetime.now()
                order_tracker.save()
            else:
                new_order_tracker_entry = OrderTracking()
                new_order_tracker_entry.status = ORDER_STATUS
                new_order_tracker_entry.status_name = STAGES[ORDER_STATUS]
                new_order_tracker_entry.created_on = datetime.now()
                new_order_tracker_entry.order_id = order_id
                new_order_tracker_entry.save()
            
        
        return redirect(order_listing_for_designer, 20)
    


@login_required
@admin_only
def update_canceled_stages(request, id):
    if request.method == 'POST':
        dispatch = request.POST.get('dispatch', '')
        dispatched = request.POST.get('dispatched', '')
        refund_amount = request.POST.get('refund_amount', '')
        fully_paid = request.POST.get('fully_paid', '')
        delivered = request.POST.get('delivered', '')
        order = Order.objects.get(id=id)
        if dispatch:
            page_name = BookingStage.ORDER_CANCELED
            ORDER_STATUS = BookingStage.ORDER_CANCELED_READY_FOR_DISPATCH
        elif dispatched:
            page_name = BookingStage.ORDER_CANCELED_READY_FOR_DISPATCH
            ORDER_STATUS = BookingStage.ORDER_CANCELED_DISPATCHED
        elif refund_amount:
            if order.pickup_date:
                page_name = BookingStage.ORDER_CANCELED_DELIVERED
            else:
                page_name = BookingStage.ORDER_CANCELED
            ORDER_STATUS = BookingStage.REFUND_INITIATED
            trans = TransactionDetails.objects.get(order_id=id)
            trans.refund_amount = refund_amount
            trans.save()
        elif fully_paid:
            page_name = BookingStage.REFUND_INITIATED
            ORDER_STATUS = BookingStage.REFUND_COMPLETED
        elif delivered:
            page_name = BookingStage.ORDER_CANCELED_DISPATCHED
            ORDER_STATUS = BookingStage.ORDER_CANCELED_DELIVERED
        update_order_status(id, ORDER_STATUS)

        order_tracker = OrderTracking.objects.filter(
                    order_id=id, status=ORDER_STATUS).last()

        if order_tracker:
            order_tracker.created_on = datetime.now()
            order_tracker.save()
        else:
            new_order_tracker_entry = OrderTracking()
            new_order_tracker_entry.status = ORDER_STATUS
            new_order_tracker_entry.status_name = STAGES[ORDER_STATUS]
            new_order_tracker_entry.created_on = datetime.now()
            new_order_tracker_entry.order_id = id
            new_order_tracker_entry.save()
        return redirect(orders_listing, page_name)
    
@login_required
@admin_only
def master_measurements(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        category_group = request.POST.get('category')
        notes = request.POST.get('notes','').strip()
        measurement_size = request.POST.getlist('measurement_size', '')
        groups = MeasurementGroups.objects.filter(category=category_group).all()
        
        user_id = order.made_by.id
        try:
            measurement = Measurement.objects.get(user_id=user_id,is_master=1, group=category_group)
            if notes:
                measurement.notes = notes
                measurement.save()
        except:
            measurement = Measurement()
            measurement.user_id = user_id
            measurement.notes = notes
            measurement.is_master = 1
            measurement.group = category_group
            measurement.save()
        
        for i, group in enumerate(groups):

            if measurement_size[i]:
                try:
                    update_data = Measurementslist.objects.get(measurement=measurement,name_id = group.id)
                    update_data.size = measurement_size[i]
                   
                    update_data.save()
                except:
                    measurementlist = Measurementslist()
                    measurementlist.measurement = measurement
                    measurementlist.name_id = group.id
                    measurementlist.size = measurement_size[i]
                    measurementlist.save()
        return redirect(order_details, id)    

@login_required
@admin_only
def add_measurements(request):
    if request.method == 'POST':
        id = request.POST.get('item_id')
        category_group = request.POST.get('category')
        orderitem =  OrderItems.objects.get(id=id)
        measurement_size = request.POST.getlist('measurement_size', '')
        notes = request.POST.get('notes','').strip()
        groups = MeasurementGroups.objects.filter(category=category_group).all()
        user_id = orderitem.order.made_by.id
        order_id = orderitem.order.id
        try:
            measurement = Measurement.objects.get(item_id=id, group=category_group)
            if notes:
                measurement.notes = notes
                measurement.save()
        except:
            measurement = Measurement()
            measurement.user_id = user_id
            measurement.notes = notes
            measurement.item_id = id
            measurement.group = category_group
            measurement.save()
        
        for i, group in enumerate(groups):

            if measurement_size[i]:
                try:
                    update_data = Measurementslist.objects.get(measurement=measurement,name_id = group.id)
                    update_data.size = measurement_size[i]
                   
                    update_data.save()
                except:
                    measurementlist = Measurementslist()
                    measurementlist.measurement = measurement
                    measurementlist.name_id = group.id
                    measurementlist.size = measurement_size[i]
                    measurementlist.save()
        return redirect(order_details, order_id)

 
@login_required
@admin_only
def upload_picked_image(request):
    if request.method == "POST":
        order_id = request.POST.get('orderId', '')
        item_id = request.POST.get('itemId', '')
        upload_item = OrderItems.objects.get(id=item_id)
        upload_item.image = request.FILES.get('itemImage', '')
        upload_item.save()
    return redirect(order_details, order_id)

        


