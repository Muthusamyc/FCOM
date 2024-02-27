import datetime

from bookings.tax import (DISIGNER_CHARGES, SHIPPING_CHARGES,
                          calculate_net_amount,
                          calculate_state_and_central_tax, calculate_taxes,
                          net_amount_without_tax)
from commons.booking_stages import STAGES, BookingStage
from dashboard.services.models import (Cart, ItemsInCart, Order, OrderItems,
                                       OrderTracking, TransactionAmount,
                                       TransactionDetails)
from fcom.settings import env

from commons.generate_order_id import generate_order_id

def create_main_order_id(cart_id, request, service_type, booking_type):
    main_order = Order(
        cart_id=cart_id,
        made_by=request.user,
        service_type_id=service_type,
        booking_type_id=booking_type,
        status=BookingStage.ORDER_INITIATED
    )
    main_order.save()
    return main_order


def move_cart_to_order(cart_id, main_order):
    cart = Cart.objects.get(id=cart_id)
    cart_items = ItemsInCart.objects.filter(cart_id=cart_id).all()
    for item in cart_items:
        order_item = OrderItems()
        order_item.product_item_id = item.item.id
        order_item.order_id = main_order.id
        order_item.qty = item.qty
        order_item.sub_total = item.sub_total
        order_item.save()
    return cart


def create_transaction(cart, main_order, payment_type):
    total_amount_without_tax = net_amount_without_tax(
        cart.estimated_price, SHIPPING_CHARGES, DISIGNER_CHARGES)
    tax_charges = calculate_taxes(total_amount_without_tax)
    csgs_and_sgst_tax = calculate_state_and_central_tax(
        total_amount_without_tax)
    net_amount = calculate_net_amount(
        cart.estimated_price, tax_charges, SHIPPING_CHARGES, DISIGNER_CHARGES)
    # save all the calculated tax into the transaction record
    transaction = TransactionDetails()
    transaction.order_id = main_order.id
    transaction.sub_total = cart.estimated_price
    transaction.taxable_order_amount = total_amount_without_tax
    transaction.calcualted_tax = tax_charges
    transaction.cgst_tax_charges = csgs_and_sgst_tax
    transaction.sgst_tax_charges = csgs_and_sgst_tax
    transaction.net_amount = net_amount
    transaction.designer_charges = DISIGNER_CHARGES
    transaction.shipping_charges = SHIPPING_CHARGES
    transaction.payment_type=payment_type
    transaction.save()
    return transaction


def create_transaction_amount(transaction, main_order, payment_type, amount, payment_gateway="PayTM"):
    transaction_amt = TransactionAmount()
    transaction_amt.transaction_id = transaction.id    
    transaction_amt.payment_amount = amount
    transaction_amt.payment_type = payment_type
    transaction_amt.order_id = main_order.id
    transaction_amt.payment_gateway = payment_gateway
    transaction_amt.save()
    transaction_amt = generate_order_id(transaction_amt, main_order, payment_type)  
    transaction_amt.save()
    return transaction_amt


def create_order_tracking(main_order, booking_stage):
    order_status_tracker = OrderTracking()
    order_status_tracker.order_id = main_order.id
    order_status_tracker.status = booking_stage
    order_status_tracker.status_name = STAGES[booking_stage]
    order_status_tracker.created_on = datetime.datetime.now()
    order_status_tracker.save()
    return order_status_tracker
