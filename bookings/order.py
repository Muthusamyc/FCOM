import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookings.helper import (create_main_order_id, create_order_tracking,
                             create_transaction, create_transaction_amount,
                             move_cart_to_order)
from bookings.payment import (get_paytm_params, verify_paytm_checksum,
                              paytm_transaction_unsuccessful, paytm_transaction_successful, remove_cart_record)

from dashboard.services.models import (
    PayTMTransactionDetails,
    Order,
    ItemsInCart,
    TransactionDetails,
    Cart,
    OrderTracking,
)
from commons.booking_stages import BookingStage, STAGES


@permission_classes([IsAuthenticated])
def create_order_redirect(request):
    try:
        global SHIPPING_CHARGES
        data = request.POST
        cart_id = data['cartId']
        payment_type = data['paymentType']
        amount = format(round(float(data['amount']), 2), ".2f")
        service_type = data['serviceType']
        booking_type = data['bookingType']

        # create a main order here, this created on every click from pay now btn
        main_order = create_main_order_id(
            cart_id=cart_id,
            request=request,
            service_type=service_type,
            booking_type=booking_type,
        )

        # get cart and itemincart to save in the order items and update order
        cart = move_cart_to_order(cart_id, main_order)

        # check service mode here
        if service_type == "2":
            SHIPPING_CHARGES = 0.0

        # calculate transaction records here
        # step 1(taxable amount): add shipping and designer charges to the estimated price
        # step 2(tax): calculate tax also cgst and sgst (state and central tax that accounts for 2.5 + 2.5 = 5%)
        # step 3(net amount) : net amount is sum of taxable amount plus tax charges
        transaction = create_transaction(cart, main_order, payment_type)

        # make payment amount this id will be sent to paytm to get the payment gateway
        # this will be linked to order through transaction record
        payment_transaction_for_order = create_transaction_amount(
            transaction, main_order, payment_type, amount)

        # track order here all its status will save in order trackign with datetime
        create_order_tracking(main_order, BookingStage.ORDER_INITIATED)

        paytm_params = get_paytm_params(
            payment_transaction_for_order.generated_order_id, amount, request.user.id)

        payment_transaction_for_order.paytm_checksum = paytm_params['CHECKSUMHASH']
        payment_transaction_for_order.save()
        return render(request, "redirect.html", paytm_params)

    except Exception as e:
        logging.error(str(e))
        return Response(
            str(e),
            status=status.HTTP_400_BAD_REQUEST
        )


@csrf_exempt
def paytm_callback_redirect(request):
    if request.method == 'POST':
        paytm_checksum = ''
        received_data = dict(request.POST)
        transId = received_data['ORDERID'][0].split('-')[-1]
        mainOrderId = received_data['ORDERID'][0].split('-')[-2]

        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]

        received_data = verify_paytm_checksum(
            paytm_params, received_data, paytm_checksum)

        if received_data['ChecksumMatched']:

            update_order = Order.objects.get(id=mainOrderId)
            transaction_record = TransactionDetails.objects.get(
                order_id=mainOrderId)
            paytm_transaction = PayTMTransactionDetails()

            paytm_transaction.payment_type = transaction_record.payment_type

            if received_data["STATUS"] == "TXN_FAILURE" and received_data['RESPCODE'] == '227':
                paytm_transaction_unsuccessful(paytm_transaction, received_data, request,
                                               mainOrderId, transaction_record, update_order, transaction_record.payment_type)
                remove_cart_record(update_order)
            elif received_data["STATUS"] == "TXN_FAILURE" and received_data['RESPCODE'] == '141':
                return redirect("cart")
            elif received_data['STATUS'] == "TXN_SUCCESS":
                paytm_transaction_successful(paytm_transaction, received_data, request, mainOrderId,
                                             transaction_record, update_order, transaction_record.payment_type)
                remove_cart_record(update_order)
            else:
                # TODO : handle what to do when payment is pending
                print("Payment Pending")
                received_data['message'] = "Payment Pending"

            response = redirect("my_booking", permanent=True)
            response.delete_cookie('itemsInCart')
            return response
        else:
            # TODO: handle what to do when checksum varification failed
            print("Checksum Mismatched")
            pass
# 1 - advance paid
# 2 - avance paid failed
# 3 - estimation paid
# 4 - estimation failed
#
