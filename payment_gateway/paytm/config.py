import requests
import json
from . import PaytmChecksum
import datetime
from fcom.settings import env

import logging

PAYTM_MID = env('PAYTM_MID')
PAYTM_MERCHANT_KEY = env('PAYTM_MERCHANT_KEY')
PAYTM_ENVIRONMENT = env('PAYTM_ENVIRONMENT')
PAYTM_WEBSITE = env('PAYTM_WEBSITE')
PAYTM_INDUSTRY_TYPE_ID = 'Retail'
PAYTM_CHANNEL_ID = 'WEB'

PAYTM_CALLBACK_URL = env('PAYTM_CALLBACK_URL')
print(PAYTM_MID)
print(PAYTM_MERCHANT_KEY)
print(PAYTM_ENVIRONMENT)
print(PAYTM_WEBSITE)

# PAYTM_MID = "Bespok98294136142537"
# PAYTM_MERCHANT_KEY = "ZBXqrrwzahu5jais"
# PAYTM_ENVIRONMENT= 'https://securegw.paytm.in'
# PAYTM_WEBSITE= 'DEFAULT'
#amount= '1.00'
#order_id ='order_'+str(datetime.datetime.now().timestamp())

def getTransactionToken(order_id, amount, customer_id=None):     
    paytmParams = dict()
    paytmParams["body"] = {
        "requestType": "Payment",
        "mid": PAYTM_MID,
        "websiteName": PAYTM_WEBSITE,
        "orderId": order_id,
        "callbackUrl": PAYTM_CALLBACK_URL,
        "txnAmount": {
            "value": amount,
            "currency": "INR",
        },
        "userInfo": {
            "custId"    : str(customer_id),
        },
    }
    print(paytmParams)
    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    checksum = PaytmChecksum.generateSignature(
        json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)

    paytmParams["head"] = {
        "signature": checksum,
    }

    post_data = json.dumps(paytmParams)

    url = PAYTM_ENVIRONMENT+"/theia/api/v1/initiateTransaction?mid=" + \
        PAYTM_MID+"&orderId="+order_id
    response = requests.post(url, data=post_data, headers={
                             "Content-type": "application/json"}).json()
    response_str = json.dumps(response)
    res = json.loads(response_str)
    if res["body"]["resultInfo"]["resultStatus"] == 'S':
        token = res["body"]["txnToken"]
    else:
        logging.error(str(res["body"]["resultInfo"]))
        token = ""
    return token


def transactionStatus(order_id):
    paytmParams = dict()
    paytmParams["body"] = {
        "mid": PAYTM_MID,
        # Enter your order id which needs to be check status for
        "orderId": order_id,
    }
    checksum = PaytmChecksum.generateSignature(
        json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)

    # head parameters
    paytmParams["head"] = {
        "signature": checksum
    }

    # prepare JSON string for request
    post_data = json.dumps(paytmParams)

    url = PAYTM_ENVIRONMENT+"/v3/order/status"

    response = requests.post(url, data=post_data, headers={
                             "Content-type": "application/json"}).json()
    response_str = json.dumps(response)
    res = json.loads(response_str)
    msg = "Transaction Status Response"
    return res['body']

def request_paytm_refund(order_id, mid, refund_id, refund_amt, txn_id):        
    paytmParams = dict()

    paytmParams["body"] = {
        "mid"          : mid, #"YOUR_MID_HERE",
        "txnType"      : "REFUND",
        "orderId"      : order_id, #"ORDERID_98765",
        "txnId"        :  txn_id, #"202005081112128XXXXXX68470101509706",
        "refId"        : refund_id, #"REFUNDID_98765",
        "refundAmount" : refund_amt #"1.00",
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "YOUR_MERCHANT_KEY")

    paytmParams["head"] = {
        "signature"    : checksum
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/refund/apply"

    # for Production
    # url = "https://securegw.paytm.in/refund/apply"
    
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    return response        
        
        
