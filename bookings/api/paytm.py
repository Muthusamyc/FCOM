from datetime import datetime
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from commons.booking_stages import BookingStage, STAGES

from dashboard.services.models import (
    PayTMTransactionDetails,
    Order,
    ItemsInCart,
    TransactionDetails,
    Cart,
    OrderTracking,
)


import logging
import json


from fcom.settings import PROJECT_ENV

#################### Paytm gateway #########################
from payment_gateway.paytm import config, PaytmChecksum


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def paytm_token(request):
    data = request.data
    order_id = data["orderId"]
    amount = data["amount"]
    user_id = request.user.id
    token = config.getTransactionToken(
        order_id=order_id, amount=amount, customer_id=user_id
    )
    return JsonResponse({"token": token}, status=200, safe=False)


@api_view(["POST"])
@csrf_exempt
def paytm_callback(request):
    try:
        mainData = request.data
        payment_type = mainData["payingFor"]
        mainOrderId = mainData["mainOrderId"]

        data = mainData["data"]
        data = json.loads(data)

        update_order = Order.objects.get(id=mainOrderId)

        transaction_record = TransactionDetails.objects.get(order_id=mainOrderId)
        paytm_trans = PayTMTransactionDetails()

        paytm_trans.payment_type = payment_type
        if data["STATUS"] == "TXN_FAILURE":
            paytm_trans.bank_txn_id = data["BANKTXNID"] if "BANKTXNID" in data else ""
            paytm_trans.checksum = data["CHECKSUMHASH"]
            paytm_trans.currency = data["CURRENCY"]
            paytm_trans.mid = data["MID"]
            paytm_trans.generated_order_id = data["ORDERID"]
            paytm_trans.response_code = data["RESPCODE"]
            paytm_trans.response_msg = data["RESPMSG"]
            paytm_trans.status = data["STATUS"]
            paytm_trans.txn_amount = data["TXNAMOUNT"]
            paytm_trans.txn_date = datetime.now()
            paytm_trans.payment_mode = (
                data["PAYMENTMODE"] if "PAYMENTMODE" in data else ""
            )
            paytm_trans.made_by = request.user
            paytm_trans.order_id = mainOrderId

            paytm_trans.save()
            transaction_record.balance_amt_due = transaction_record.net_amount
            transaction_record.paymtent_status = "Paymet Failed"
            transaction_record.save()
            if payment_type == "advance":
                update_order.is_advance_paid = False
            if payment_type == "estimated":
                update_order.is_estimation_paid = False

            update_order.status = BookingStage.ORDER_FAILED
            update_order.save()

            order_tracker = OrderTracking()
            order_tracker.order_id = update_order.id
            order_tracker.status = BookingStage.ORDER_FAILED
            order_tracker.status_name = STAGES[BookingStage.ORDER_FAILED]
            order_tracker.save()

            return JsonResponse(
                {
                    "message": "failed",
                    "orderId": data["ORDERID"],
                    "orderDate": update_order.created_on,
                    "status": "Failed",
                    # "estimatedAmount" : update_order.cart.estimated_price,
                    # "advanceAmount" : update_order.cart.advance_payable,
                    # "paymentType" : payment_type,
                },
                status=200,
                safe=False,
            )
        else:
            paytm_trans.bank_name = data["BANKNAME"] if "BANKNAME" in data else ""
            paytm_trans.bank_txn_id = data["BANKTXNID"] if "BANKTXNID" in data else ""
            paytm_trans.checksum = (
                data["CHECKSUMHASH"] if "CHECKSUMHASH" in data else ""
            )
            paytm_trans.currency = data["CURRENCY"]
            paytm_trans.mid = data["MID"]
            paytm_trans.generated_order_id = data["ORDERID"]
            paytm_trans.response_code = data["RESPCODE"]
            paytm_trans.response_msg = data["RESPMSG"]
            paytm_trans.gateway_name = (
                data["GATEWAYNAME"] if "GATEWAYNAME" in data else ""
            )
            paytm_trans.status = data["STATUS"]
            paytm_trans.txn_amount = data["TXNAMOUNT"]
            paytm_trans.txn_date = data["TXNDATE"]
            paytm_trans.txn_id = data["TXNID"]
            paytm_trans.payment_mode = (
                data["PAYMENTMODE"] if "PAYMENTMODE" in data else ""
            )
            paytm_trans.made_by = request.user
            paytm_trans.order_id = mainOrderId
            paytm_trans.save()

            order_tracker = OrderTracking()
            order_tracker.order_id = update_order.id

            if payment_type == "advance" or payment_type == "estimated":
                cartId = mainData["cartId"]
                cart = Cart.objects.get(id=cartId)
                items = ItemsInCart.objects.filter(cart_id=cart.id).all()
                items.delete()

            if payment_type == "advance":
                transaction_record.advance_paid_amount = data["TXNAMOUNT"]
                # transaction_record.net_amount = transaction_record.net_amount - float(data['TXNAMOUNT'])
                transaction_record.balance_amt_due = (
                    transaction_record.net_amount - float(data["TXNAMOUNT"])
                )
                transaction_record.paymtent_status = "Partial Paid"
                update_order.is_advance_paid = True
                update_order.status = BookingStage.ORDER_BOOKED

                order_tracker.status = BookingStage.ORDER_BOOKED
                order_tracker.status_name = STAGES[BookingStage.ORDER_BOOKED]
                order_tracker.created_on = datetime.now()
                order_tracker.save()
                cart.delete()

            if payment_type == "estimated":
                transaction_record.estimation_paid_amount = data["TXNAMOUNT"]
                transaction_record.balance_amt_due = (
                    transaction_record.net_amount - float(data["TXNAMOUNT"])
                )
                # transaction_record.net_amount = transaction_record.net_amount - float(data['TXNAMOUNT'])
                transaction_record.paymtent_status = "Estimation Paid"
                update_order.is_estimation_paid = True
                update_order.status = BookingStage.ORDER_BOOKED

                order_tracker.status = BookingStage.ORDER_BOOKED
                order_tracker.status_name = STAGES[BookingStage.ORDER_BOOKED]
                order_tracker.created_on = datetime.now()
                order_tracker.save()
                cart.delete()

            if payment_type == "balance":
                transaction_record.estimation_paid_amount = data["TXNAMOUNT"]
                transaction_record.balance_amt_due = (
                    transaction_record.balance_amt_due - float(data["TXNAMOUNT"])
                )
                # transaction_record.net_amount = transaction_record.net_amount - float(data['TXNAMOUNT'])
                transaction_record.paymtent_status = "Total Paid"
                update_order.is_total_paid = True
                update_order.status = BookingStage.BALANCE_AMOUNT_PAID

            update_order.save()
            transaction_record.save()

            return JsonResponse(
                {
                    "message": "failed",
                    "orderId": data["ORDERID"],
                    "orderDate": update_order.created_on,
                    "status": "Order Booked",
                    # "estimatedAmount" : update_order.cart.estimated_price,
                    # "advanceAmount" : update_order.cart.advance_payable,
                    # "paymentType" : payment_type,
                },
                status=200,
                safe=False,
            )
    except Exception as e:
        with open("data/paytm_transaction.json", "a") as file:
            json.dump(data, file, indent=2)
        logging.error(str(e))
        return JsonResponse({"message": "error"}, status=400, safe=False)
