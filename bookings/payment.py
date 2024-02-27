import datetime

from commons.booking_stages import STAGES, BookingStage
from dashboard.services.models import (
    Cart,
    ItemsInCart,
    Order,
    OrderTracking,
    PayTMTransactionDetails,
    TransactionDetails,
)
from payment_gateway.paytm import config
from payment_gateway.paytm.paytm_methods import (
    generate_checksum,
    verify_checksum,
    verify_checksum_by_str,
)


from fcom.settings import env


def get_paytm_params(order_id, amount, user, payment_type="advance"):
    callback_url = ""
    environment = env("ENV")
    if environment == "production":
        if payment_type == "advance" or payment_type == "estimated":
            callback_url = "https://www.fcomindia.com/bookings/paytm-callback-redirect/"
        if payment_type == "balance":
            callback_url = "https://www.fcomindia.com/bookings/paytm-callback-transaction-redirect/"
    else:
        if payment_type == "advance" or payment_type == "estimated":
            callback_url = "http://127.0.0.1:8000/bookings/paytm-callback-redirect/"
        if payment_type == "balance":
            callback_url = "http://127.0.0.1:8000/bookings/paytm-callback-transaction-redirect/"

    params = (
        ("MID", config.PAYTM_MID),
        ("ORDER_ID", str(order_id)),
        ("CUST_ID", str(user)),
        ("TXN_AMOUNT", str(amount)),
        ("CHANNEL_ID", config.PAYTM_CHANNEL_ID),
        ("WEBSITE", config.PAYTM_WEBSITE),
        ("INDUSTRY_TYPE_ID", config.PAYTM_INDUSTRY_TYPE_ID),
        ("CALLBACK_URL", callback_url),
    )
    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, config.PAYTM_MERCHANT_KEY)
    paytm_params["CHECKSUMHASH"] = checksum
    return paytm_params


def verify_paytm_checksum(paytm_params, received_data, paytm_checksum):
    for key, value in received_data.items():
        if key == "CHECKSUMHASH":
            paytm_checksum = value[0]
        else:
            paytm_params[key] = str(value[0])
    # Verify checksum
    is_valid_checksum = verify_checksum(
        paytm_params, config.PAYTM_MERCHANT_KEY, str(paytm_checksum)
    )
    if is_valid_checksum:
        paytm_params["ChecksumMatched"] = True
    else:
        paytm_params["ChecksumMatched"] = False

    return paytm_params


def paytm_transaction_unsuccessful(
    paytm_transaction,
    recieved_data,
    request,
    mainOrderId,
    transaction_record,
    update_order,
    payment_type,
):
    paytm_transaction.bank_txn_id = (
        recieved_data["BANKTXNID"] if "BANKTXNID" in recieved_data else ""
    )
    # paytm_transaction.checksum = recieved_data["CHECKSUMHASH"]
    paytm_transaction.currency = recieved_data["CURRENCY"]
    paytm_transaction.mid = recieved_data["MID"]
    paytm_transaction.generated_order_id = recieved_data["ORDERID"]
    paytm_transaction.response_code = recieved_data["RESPCODE"]
    paytm_transaction.response_msg = recieved_data["RESPMSG"]
    paytm_transaction.status = recieved_data["STATUS"]
    paytm_transaction.txn_amount = recieved_data["TXNAMOUNT"]
    paytm_transaction.txn_date = (
        recieved_data["TXNDATE"] if "TXNDATE" in recieved_data else None
    )
    paytm_transaction.payment_mode = (
        recieved_data["PAYMENTMODE"] if "PAYMENTMODE" in recieved_data else ""
    )
    paytm_transaction.made_by = request.user
    paytm_transaction.order_id = mainOrderId
    paytm_transaction.save()
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
    return update_order


def paytm_transaction_successful(
    paytm_transaction,
    recieved_data,
    request,
    mainOrderId,
    transaction_record,
    update_order,
    payment_type,
):
    paytm_transaction.bank_name = (
        recieved_data["BANKNAME"] if "BANKNAME" in recieved_data else ""
    )
    paytm_transaction.bank_txn_id = (
        recieved_data["BANKTXNID"] if "BANKTXNID" in recieved_data else ""
    )
    paytm_transaction.checksum = (
        recieved_data["CHECKSUMHASH"] if "CHECKSUMHASH" in recieved_data else ""
    )
    paytm_transaction.currency = recieved_data["CURRENCY"]
    paytm_transaction.mid = recieved_data["MID"]
    paytm_transaction.generated_order_id = recieved_data["ORDERID"]
    paytm_transaction.response_code = recieved_data["RESPCODE"]
    paytm_transaction.response_msg = recieved_data["RESPMSG"]
    paytm_transaction.gateway_name = (
        recieved_data["GATEWAYNAME"] if "GATEWAYNAME" in recieved_data else ""
    )
    paytm_transaction.status = recieved_data["STATUS"]
    paytm_transaction.txn_amount = recieved_data["TXNAMOUNT"]
    paytm_transaction.txn_date = recieved_data["TXNDATE"]
    paytm_transaction.txn_id = recieved_data["TXNID"]
    paytm_transaction.payment_mode = (
        recieved_data["PAYMENTMODE"] if "PAYMENTMODE" in recieved_data else ""
    )
    paytm_transaction.made_by = request.user
    paytm_transaction.order_id = update_order.id
    paytm_transaction.save()
    order_tracker = OrderTracking()
    order_tracker.order_id = update_order.id
    # if payment_type == "advance" or payment_type == "estimated":
    #     cartId = update_order.cart_id
    #     cart = Cart.objects.get(id=cartId)
    #     items = ItemsInCart.objects.filter(cart_id=cart.id).all()
    #     items.delete()
    if payment_type == "advance":
        transaction_record.advance_paid_amount = recieved_data["TXNAMOUNT"]
        # transaction_record.net_amount = transaction_record.net_amount - float(data['TXNAMOUNT'])
        transaction_record.balance_amt_due = transaction_record.net_amount - float(
            recieved_data["TXNAMOUNT"]
        )
        transaction_record.paymtent_status = "Advance Paid"
        update_order.is_advance_paid = True
        update_order.status = BookingStage.ORDER_BOOKED
        order_tracker.status = BookingStage.ORDER_BOOKED
        order_tracker.status_name = STAGES[BookingStage.ORDER_BOOKED]
        order_tracker.created_on = datetime.datetime.now()
        order_tracker.save()
        # cart.delete()
    if payment_type == "estimated":
        transaction_record.estimation_paid_amount = recieved_data["TXNAMOUNT"]
        transaction_record.balance_amt_due = transaction_record.net_amount - float(
            recieved_data["TXNAMOUNT"]
        )
        # transaction_record.net_amount = transaction_record.net_amount - float(data['TXNAMOUNT'])
        transaction_record.paymtent_status = "Estimation Paid"
        update_order.is_estimation_paid = True
        update_order.status = BookingStage.ORDER_BOOKED
        order_tracker.status = BookingStage.ORDER_BOOKED
        order_tracker.status_name = STAGES[BookingStage.ORDER_BOOKED]
        order_tracker.created_on = datetime.datetime.now()
        order_tracker.save()
        # cart.delete()
    if payment_type == "balance":
        transaction_record.estimation_paid_amount = recieved_data["TXNAMOUNT"]
        transaction_record.balance_amt_due = transaction_record.balance_amt_due - float(
            recieved_data["TXNAMOUNT"]
        )
        # transaction_record.net_amount = transaction_record.net_amount - float(data['TXNAMOUNT'])
        transaction_record.paymtent_status = "Total Paid"
        update_order.is_total_paid = True
        update_order.status = BookingStage.BALANCE_AMOUNT_PAID
    update_order.save()
    transaction_record.save()


def remove_cart_record(order):
    cart = Cart.objects.get(id=order.cart_id)
    items = ItemsInCart.objects.filter(cart_id=cart.id).all()
    items.delete()
    cart.delete()
    return True
