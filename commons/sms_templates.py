from fcom.settings import env
import requests
def send_sms_notification(number, message):
    url = "https://1.rapidsms.co.in/api/push.json"
    api = env("RAPID_SMS_API_KEY")
    querystring = { "apikey":api,"sender":"FCOMID","text":message,"mobileno":number}
    headers = {
        'cache-control': "no-cache"
    }
    return requests.request("GET", url, headers=headers, params=querystring)

def registration(mobile_no, otp):
    message = f'Dear customer, use {otp} as OTP for FcomIndia registration'
    resp = send_sms_notification(mobile_no, message)
    return resp

def mobile_login(mobile_no, customer_name, otp):
    message = f'Dear {customer_name}, use {otp} as OTP for FcomIndia Login'
    resp = send_sms_notification(mobile_no, message)
    return resp

def visit_consult_sms(mobile_no, visit_date):
    message = f'Thanks for choosing FCOM. Our representative is planning to visit you on {visit_date} to collect the order. Call 9108902222 for queries'
    resp = send_sms_notification(mobile_no, message)
    return resp
def waiting_for_approval_sms(mobile_no, order_id):
    message = f'Please visit your order {order_id} https://fcomindia.com/bookings/order-history/{order_id} to approve estimated cost. Only after the approval, order will be executed. Call FCOM 9108902222 for queries'
    resp = send_sms_notification(mobile_no, message)
    return resp

def dispatch_status(mobile_no, order_id):
    message = f'Your order {order_id}Link https://fcomindia.com/bookings/order-history/{order_id} is complete and ready for dispatch. Request you to make full payment. Call FCOM 9108902222 for queries'
    resp = send_sms_notification(mobile_no, message)
    return resp


def dispatched_sms(mobile_no,order_id):
    message = f'Your order {order_id} Link https://fcomindia.com/bookings/order-history/{order_id} is dispatched. Leave your {order_id} Link https://fcomindia.com/bookings/my-bookings/ .Call FCOM 9108902222 for queries'
    resp = send_sms_notification(mobile_no, message)
    return resp
    


