import logging
import random
import threading

import requests
from django.contrib.auth import login
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from dashboard.master.models import User
from fcom.settings import env

from commons.mail.email_config import login_mail_otp
from commons.sms_templates import *



                                                                                 
@api_view(['POST'])
@permission_classes([AllowAny])
def send_login_otp(request):  
    if request.method == 'POST':
        data = request.data
        user_id = data['userId']
        status = 0
        
        try:
            if "@" in user_id:
                user_record = User.objects.get(email=user_id)
                request.session['user_id'] = user_id  
                request.session['login_type'] = "email"                
            else:
                user_record = User.objects.get(mobile_no=user_id)
                request.session['user_id'] = user_id
                request.session['login_type'] = "mobile"
        except Exception as e:            
            logging.exception(str(e))
            return JsonResponse({"status" : "newuser"}, status=200, safe=False)
        
        if user_record:   
            user_name = user_record.first_name+' '+ user_record.last_name         
            otp = random.randint(100000,999999)                 
            if env('ENV') == "development":                
                status = 1
                print(f"OTP: {otp}")
            else:                   
                if "@" in user_id:
                    tread = threading.Thread(target=login_mail_otp, args=[otp,user_id,user_name])
                    tread.start()
                    status = 1
                else:
                    resp = mobile_login(user_record.mobile_no, user_record.first_name, otp).json()
                
            if (status == 1 or resp['status'] == "success"):              
                request.session['login_otp'] = otp
                return JsonResponse({'status': 'ok', 'mobileNo' : user_id}, status=200, safe=False)
            else:
                if resp:
                    print(resp['status'])
                return JsonResponse({'status': 'failed'}, status=200, safe=False)
        else:
            return JsonResponse({'status': 'invalid'}, status=200, safe=False)          


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    if request.method == "POST":
        otp = request.data['otp']
        if int(otp) == request.session.get('login_otp'):
            #user = authenticate(request=request, email=request.session.get("username"), password=request.session.get('password'))
            login_type = request.session.get('login_type')
            if login_type == 'mobile':
                user = User.objects.get(mobile_no=request.session['user_id'])
            else:
                user = User.objects.get(email=request.session['user_id'])
            user.backend = 'django.contrib.auth.backends.ModelBackend'
           
            
            if user:
                login(request=request, user=user)
                
                return JsonResponse(
                    {
                        'status': 'success',
                        "isDetailsAdded" : user.is_details_added,
                        "isPasswordSet" : user.is_password_set
                    },
                    status=200, safe=False)
            else:
                return JsonResponse(
                    {
                        'status': 'loggingFailed'
                    },
                    status=200, safe=False
                )
        else:
            return JsonResponse({'status' : 'failed'}, status=200, safe=False)