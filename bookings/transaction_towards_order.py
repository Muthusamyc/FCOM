import requests
import datetime
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect

from dashboard.services.models import Order, OrderTracking, TransactionDetails, OrderItems, Cart, ItemsInCart, TransactionAmount, CustomerReview
from commons.booking_stages import BookingStage, STAGES
from fcom.settings import env
from commons.generate_order_id import generate_order_id

from bookings.payment import (get_paytm_params, verify_paytm_checksum,
                              paytm_transaction_unsuccessful, paytm_transaction_successful, remove_cart_record)

from dashboard.services.models import (
    PayTMTransactionDetails)

from .helper import create_transaction_amount, create_order_tracking

@permission_classes([IsAuthenticated])
def create_transaction_towards_order(request):
    data = request.POST
    order_id = data['orderId']
    payment_type = data['paymentType']
    amount = format(round(float(data['amount']), 2), ".2f")

    main_order = Order.objects.get(id=order_id)

    order_transaction = TransactionDetails.objects.get(order_id=main_order.id)
    order_transaction.payment_type = payment_type
    order_transaction.save()
    
    amount_trans_for_order = create_transaction_amount(order_transaction, main_order, payment_type, amount)

    paytm_params = get_paytm_params(
        amount_trans_for_order.generated_order_id, amount, request.user.id, payment_type)

    amount_trans_for_order.paytm_checksum = paytm_params['CHECKSUMHASH']
    amount_trans_for_order.save()   
    
    return render(request, "redirect-balance.html", paytm_params)


@csrf_exempt
def paytm_callback_trasaction_for_order_redirect(request):
    if request.method == 'POST':
        paytm_checksum = ''
        received_data = dict(request.POST)
        
        mainOrderId = received_data['ORDERID'][0].split('-')[-2]
        transId = received_data['ORDERID'][0].split('-')[-1]

        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]

        received_data = verify_paytm_checksum(
            paytm_params, received_data, paytm_checksum)

        if received_data['ChecksumMatched']:
            transaction_record = TransactionDetails.objects.get(
                order_id=mainOrderId)
            
            update_order = Order.objects.get(id=transaction_record.order_id)
            
            paytm_transaction = PayTMTransactionDetails()

            paytm_transaction.payment_type = transaction_record.payment_type

            if received_data["STATUS"] == "TXN_FAILURE" and received_data['RESPCODE'] == '227':
                paytm_transaction_unsuccessful(paytm_transaction, received_data, request,
                                               mainOrderId, transaction_record, update_order, transaction_record.payment_type)
                
            elif received_data["STATUS"] == "TXN_FAILURE" and received_data['RESPCODE'] == '141':
                return redirect("my_booking")
            elif received_data['STATUS'] == "TXN_SUCCESS":
                paytm_transaction_successful(paytm_transaction, received_data, request, mainOrderId,
                                             transaction_record, update_order, transaction_record.payment_type) 
                create_order_tracking(update_order, BookingStage.BALANCE_AMOUNT_PAID)               
            else:
                # TODO : handle what to do when payment is pending
                print("Payment Pending")
                received_data['message'] = "Payment Pending"
            return redirect("my_booking", permanent=True)            
        else:
            # TODO: handle what to do when checksum varification failed
            print("Checksum Mismatched")
            pass
