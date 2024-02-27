import requests
import datetime
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from dashboard.services.models import Order, OrderTracking, TransactionDetails, OrderItems, Cart, ItemsInCart, TransactionAmount, CustomerReview
from payment_gateway.paytm import config, PaytmChecksum
from commons.booking_stages import BookingStage ,STAGES
from fcom.settings import env


import logging



TAX_PERCENTAGE = 5
SHIPPING_CHARGES = 99
DISIGNER_CHARGES = 50

CGST_TAX = 2.5
SGST_TAX = 2.5

def calculate_taxes(amount):
    tax_charges = float(amount) * (TAX_PERCENTAGE / 100)
    return round(tax_charges, 2)

def calculate_state_and_central_tax(amount):
    tax = float(amount) * (CGST_TAX / 100)
    return  round(tax, 2)

def net_amount_without_tax(estimated_amount, shipping_charges, designer_charges):
    return round(float(estimated_amount) + float(shipping_charges) + float(designer_charges))


def calculate_net_amount(amount, tax, shipping_charges, designer_charges):
    return round((float(amount) + tax + float(shipping_charges) +  float(designer_charges)), 2)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        global SHIPPING_CHARGES        
        data = request.data
        cart_id = data['cartId']
        payment_type = data['paymentType']
        amount = format(round(float(data['amount']), 2), ".2f")
        service_type = data['serviceType']
        booking_type = data['bookingType']

        #create a main order here, this created on every click from pay now btn 
        main_order = Order(
            cart_id = cart_id,
            made_by = request.user,
            service_type_id = service_type,
            booking_type_id = booking_type,
            status = BookingStage.ORDER_INITIATED
        )
        main_order.save()

        # get cart and itemincart to save in the order items and update order 
        cart = Cart.objects.get(id=cart_id)       
        cart_items = ItemsInCart.objects.filter(cart_id=cart_id).all()
        for item in cart_items:
            order_item = OrderItems()
            order_item.product_item_id = item.item.id
            order_item.order_id = main_order.id
            order_item.qty = item.qty
            order_item.sub_total = item.sub_total
            order_item.save()
            
        #check service mode here
        
        if service_type == "2":
            SHIPPING_CHARGES = 0.0            

        #calculate transaction records here 
        # step 1(taxable amount): add shipping and designer charges to the estimated price
        # step 2(tax): calculate tax also cgst and sgst (state and central tax that accounts for 2.5 + 2.5 = 5%)        
        # step 3(net amount) : net amount is sum of taxable amount plus tax charges 
        total_amount_without_tax = net_amount_without_tax(cart.estimated_price, SHIPPING_CHARGES, DISIGNER_CHARGES)        
        tax_charges = calculate_taxes(total_amount_without_tax)
        csgs_and_sgst_tax = calculate_state_and_central_tax(total_amount_without_tax)
        net_amount = calculate_net_amount(cart.estimated_price, tax_charges, SHIPPING_CHARGES, DISIGNER_CHARGES)
        
        #save all the calculated tax into the transaction record 
        transaction = TransactionDetails()
        transaction.order_id = main_order.id        
        transaction.sub_total = cart.estimated_price
        transaction.taxable_order_amount = total_amount_without_tax
        transaction.calcualted_tax = tax_charges
        transaction.cgst_tax_charges = csgs_and_sgst_tax
        transaction.sgst_tax_charges = csgs_and_sgst_tax
        transaction.net_amount  = net_amount
        transaction.designer_charges = DISIGNER_CHARGES
        transaction.shipping_charges = SHIPPING_CHARGES
        transaction.save()

        # make payment amount this id will be sent to paytm to get the payment gateway
        # this will be linked to order through transaction record 
        payment_transaction_for_order = TransactionAmount()
        payment_transaction_for_order.transaction_id = transaction.id
        payment_transaction_for_order.payment_type = payment_type
        payment_transaction_for_order.payment_amount = amount
        
        ENV = env('ENV')
        if ENV == 'development':
            payment_transaction_for_order.generated_order_id = "FCOM-STAGGING-" + f"{main_order.id:03}"
        elif ENV == "localdevelopement":
            DEVELOPER = env('DEVELOPER')
            payment_transaction_for_order.generated_order_id = f"FCOM-STAGGING-DEV-{DEVELOPER}-" + f"{main_order.id:03}"
        else:
            #production env
            payment_transaction_for_order.generated_order_id = "FCOMIINDIA-" + f"{main_order.id:03}"

        payment_transaction_for_order.save()

        #track order here all its status will save in order trackign with datetime 
        order_status_tracker = OrderTracking()
        order_status_tracker.order_id = main_order.id
        order_status_tracker.status = BookingStage.ORDER_INITIATED
        order_status_tracker.status_name = STAGES[BookingStage.ORDER_INITIATED]
        order_status_tracker.created_on = datetime.datetime.now()
        order_status_tracker.save()
        
        token = config.getTransactionToken(str(payment_transaction_for_order.generated_order_id), amount=amount, customer_id=request.user.id)
        return Response(
            {
                'mainOrderId' : main_order.id,
                'orderId' : payment_transaction_for_order.generated_order_id,
                'token' : token,
                'amount' : amount
            }, status=status.HTTP_200_OK)
    except Exception as e:
        logging.error(str(e))
        return Response(
            str(e),
            status=status.HTTP_400_BAD_REQUEST
        )


# 1 - advance paid 
# 2 - avance paid failed
# 3 - estimation paid 
# 4 - estimation failed
#


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction_towards_order(request):
    data = request.data
    order_id = data['orderId']
    payment_type = data['paymentType']
    amount = format(round(float(data['amount']), 2), ".2f")

    main_order = Order.objects.get(id=order_id)
    #old_transaction = TransactionDetails.objects.filter(order_id=main_order.id).last()

    transacation_order =  TransactionDetails.objects.get(order_id=main_order.id) 
    # transacation_order.payment_type = payment_type
    # transacation_order.payment_amount = amount
    # transacation_order.sub_total = old_transaction.sub_total
    # transacation_order.calcualted_tax = old_transaction.calcualted_tax
    # transacation_order.net_amount = old_transaction.net_amount
    # transacation_order.designer_charges = old_transaction.designer_charges
    # transacation_order.shipping_charges = old_transaction.shipping_charges
    #transacation_order.save()

    transaction_amount_for_order = TransactionAmount()
    transaction_amount_for_order.transaction_id = transacation_order.id
    transaction_amount_for_order.payment_amount = amount
    transaction_amount_for_order.payment_type = payment_type
    
    transaction_amount_for_order.save()
    
    ENV = env('ENV')
    if ENV == 'development':
            transaction_amount_for_order.generated_order_id = "FCOM-STAGGING-UPDATED-" + f"{transaction_amount_for_order.id:03}"
    elif ENV == "localdevelopement":
        developer = env('DEVELOPER')
        transaction_amount_for_order.generated_order_id = f"FCOM-STAGGING-BALANCE-{developer}" + f"{transaction_amount_for_order.id:03}"
    else:
        #production env
        transaction_amount_for_order.generated_order_id = "FCOMIINDIA-BALANCE-" + f"{main_order.id:03}"

    transaction_amount_for_order.save()
    
    order_status_tracker = OrderTracking()
    order_status_tracker.order_id = main_order.id
    order_status_tracker.status = BookingStage.BALANCE_AMOUNT_PAID
    order_status_tracker.status_name = STAGES[BookingStage.BALANCE_AMOUNT_PAID]
    order_status_tracker.created_on = datetime.datetime.now()
    order_status_tracker.save()
    
    token = config.getTransactionToken(str(transaction_amount_for_order.generated_order_id), amount=amount, customer_id=request.user.id)
    return Response(
            {
                'mainOrderId' : main_order.id,
                'orderId' : transaction_amount_for_order.generated_order_id,
                'token' : token,
                'amount' : amount,
                "payingFor" : payment_type
            }, status=status.HTTP_200_OK)   



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def cancel_order(request):
    data = request.data
    order = Order.objects.get(id=data['orderId'])
    order.status = BookingStage.ORDER_CANCELED
    order.is_order_cancaled = 1
    order.save()
    order_status_tracker = OrderTracking()
    order_status_tracker.order_id = data['orderId']
    order_status_tracker.status = BookingStage.ORDER_CANCELED
    order_status_tracker.status_name = STAGES[BookingStage.ORDER_CANCELED]
    order_status_tracker.created_on = datetime.datetime.now()
    order_status_tracker.save()

    return JsonResponse(
        {
            'orderId' : order.id,
            'status' : STAGES[BookingStage.ORDER_CANCELED]

        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def approval_accepted_estimation(request):
    data = request.data
    order = Order.objects.get(id=data['orderId'])
    order.invoice_date = datetime.date.today()
    order.status = BookingStage.APPROVAL_ACCEPTED
    order.is_order_approved = True
    order.save()
    order_status_tracker = OrderTracking()
    order_status_tracker.order_id = data['orderId']
    order_status_tracker.status = BookingStage.APPROVAL_ACCEPTED
    order_status_tracker.status_name = STAGES[BookingStage.APPROVAL_ACCEPTED]
    order_status_tracker.created_on = datetime.datetime.now()
    order_status_tracker.save()
    return JsonResponse(
        {
            'orderId' : order.id,
            'status' : STAGES[BookingStage.APPROVAL_ACCEPTED]

        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delivery_confirmed(request):
    data = request.data
    order_id = data['orderId']
    order = Order.objects.get(id=order_id)
    order.status = BookingStage.ORDER_DELIVERED
    order.is_order_delivered = True
    order.save()
    order_status_tracker = OrderTracking()
    order_status_tracker.order_id = order_id
    order_status_tracker.status = BookingStage.ORDER_DELIVERED
    order_status_tracker.status_name = STAGES[BookingStage.ORDER_DELIVERED]
    order_status_tracker.created_on = datetime.datetime.now()
    order_status_tracker.save()
  
        

    return JsonResponse(
        {
            'orderId' : order.id,
            'status' : STAGES[BookingStage.ORDER_DELIVERED]

        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def approval_rejected_estimation(request):
    data = request.data
    order = Order.objects.get(id=data['orderId'])
    order.status = BookingStage.APPROVAL_REJECTED
    order.is_order_approved = False
    order.save()
    order_status_tracker = OrderTracking()
    order_status_tracker.order_id = data['orderId']
    order_status_tracker.status = BookingStage.APPROVAL_REJECTED
    order_status_tracker.status_name = STAGES[BookingStage.APPROVAL_REJECTED]
    order_status_tracker.created_on = datetime.datetime.now()
    order_status_tracker.save()
    return JsonResponse(
        {
            'orderId' : order.id,
            'status' : STAGES[BookingStage.APPROVAL_REJECTED]

        })



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def remove_order_item(request):
    data = request.data
    item_id = data['orderId']
    removal_item = OrderItems.objects.get(id=item_id)
    item_count =  OrderItems.objects.filter(order_id=removal_item.order_id,status=1).count()
    

    if item_count > 1:

        removal_item_sub_total = removal_item.sub_total * removal_item.qty

        update_related_transaction = TransactionDetails.objects.get(order_id=removal_item.order_id)

        new_sub_total = (update_related_transaction.sub_total - removal_item_sub_total)
        update_related_transaction.sub_total = new_sub_total

        taxable_amount = new_sub_total + update_related_transaction.designer_charges + \
            update_related_transaction.shipping_charges + \
            update_related_transaction.extra_material
        tax_charges = calculate_taxes(taxable_amount)
        net_amount = taxable_amount + tax_charges

        update_related_transaction.net_amount = net_amount

        update_related_transaction.calcualted_tax = tax_charges
        update_related_transaction.taxable_order_amount = taxable_amount
        update_related_transaction.balance_amt_due = net_amount - \
            (update_related_transaction.estimation_paid_amount +
                update_related_transaction.advance_paid_amount)
        update_related_transaction.save()
        
        removal_item.status = 0
        removal_item.save()
        statusmsg = 'item_removed'
    else:
        
        last_order = Order.objects.get(id=removal_item.order_id)
        last_order.status = BookingStage.ORDER_CANCELED
        last_order.is_order_cancaled = 1
        last_order.save()
        removal_item.status = 0
        removal_item.save()
        statusmsg = 'canceled_order'
        order_status_tracker = OrderTracking()
        order_status_tracker.order_id = last_order.id
        order_status_tracker.status = BookingStage.ORDER_CANCELED
        order_status_tracker.status_name = STAGES[BookingStage.ORDER_CANCELED]
        order_status_tracker.created_on = datetime.datetime.now()
        order_status_tracker.save()



    return JsonResponse(
        {
            'orderId' : removal_item.id,
            'status' : statusmsg

        })



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def customer_review(request):
    data = request.data
    order = Order.objects.get(id=data['orderId'])
    reviews = CustomerReview()
    reviews.order = order
    reviews.review =data['review']
    reviews.customer_services =data['customer_services']
    reviews.designer =data['designer']
    reviews.delivery_services =data['delivery_services']

    reviews.save()
    return JsonResponse(
        {
            'orderId' : order.id,
            'status' : 'success'

        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def reshedule_visitdate(request):
    data = request.data
    order = Order.objects.get(id=data['orderId'])
    order.consultation_date = data['fromDate']
    order.save()
    return JsonResponse(
        {
            'orderId' : order.id,
            'status' : 'success'

        })