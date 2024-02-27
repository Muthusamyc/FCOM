import requests
import random
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from dashboard.master.models import User, UserDetail
from commons.roles import ROLE_CHOICES, CUSTOMER
import threading

from commons.mail.email_config import signup_mail_otp
from commons.sms_templates import *



@api_view(['POST'])
@permission_classes([AllowAny])
def send_signup_otp(request):
    if request.method == "POST":
        mobile_no = request.data['signUpOtpMobileNumber']        
        otp = random.randint(100000,999999)     
        print(otp)
        request.session['singup_otp'] = otp
        request.session['mobile_no'] = mobile_no
        status = 0
        if "@" in mobile_no:
            is_user_exist = User.objects.filter(email=mobile_no).exists() 
            if is_user_exist:
                return JsonResponse({'status' : 'duplicate', 'message' : 'mobile number exits'})  
            tread = threading.Thread(target=signup_mail_otp, args=[otp,mobile_no])
            tread.start()

            status = 1
        else:
            is_user_exist = User.objects.filter(mobile_no=mobile_no).exists()
            if is_user_exist:
                return JsonResponse({'status' : 'duplicate', 'message' : 'mobile number exits'})   
            resp = registration(mobile_no, otp).json()
        if (status == 1 or resp['status'] == "success"):  
            request.session['singup_otp'] = otp
        return JsonResponse({'status' : "success", 'mobileNo' : mobile_no}, status=200, safe=False)

@api_view(['POST'])
@permission_classes([AllowAny]) 
def verify_singup_otp(request):
    if request.method == "POST":
        otp = request.data['otp']
        if int(otp) == request.session.get('singup_otp'):
            userdata = request.session.get('mobile_no')
            try:
                if "@" in userdata:
                    new_uer = User(email=userdata, is_details_added=False, is_password_set=False, role=CUSTOMER)
                    new_uer.backend = 'django.contrib.auth.backends.ModelBackend'               
                    new_uer.save()
                    login(request, new_uer)

                else:
                    new_uer = User(mobile_no=userdata, is_details_added=False, is_password_set=False, role=CUSTOMER)
                    new_uer.backend = 'django.contrib.auth.backends.ModelBackend'               
                    new_uer.save()
                    login(request, new_uer)
            except IntegrityError as e: 
                logging.error(str(e.args[0]))
                return JsonResponse({'status' : 'duplicate', 'message' : 'mobile number exits'})
                
            return JsonResponse({'status' : 'success'}, status=200, safe=False)


@api_view(['POST'])
@permission_classes([AllowAny]) 
def set_singup_password(request):
    if request.method == "POST":
        password = request.data['password']
        mobile_no = request.session.get('mobile_no')
        if "@" in mobile_no:
            user = User.objects.get(email=mobile_no)
        else:
            user = User.objects.get(mobile_no=mobile_no)

        if user:
            user.set_password(password)  
            user.is_password_set = True          
            user.save()
            return JsonResponse({'status' : 'success', 'mobile_no' : mobile_no}, status=200, safe=False)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_add_details(request):
    """
        This method is to signup new users from the client side application
    """
    if request.method == 'POST':
        data = request.data
        user_data = data['sigupModalInfo']
        print(user_data)
        try:
            if request.user.is_authenticated:                    
                new_user = User.objects.get(id=request.user.id)        
            else:
                if "@" in user_data:
                    new_user = User.objects.get(email=user_data)
                    new_user.mobile_no = data['mobile_no']
                else:
                    new_user = User.objects.get(mobile_no=user_data)
                    new_user.email = data['email']
                
            new_user.last_name = data['lastName']
            new_user.first_name = data['firstName']
            new_user.is_details_added = True                
            new_user.save()
            # new_user = SignUpUser(
            #     first_name = data['firstName'],
            #     last_name = data['lastName'],
            #     email = data['email'],
            #     username = data['email'],
            #     password = data['password'],
            #     role = data['userType']
            # )
            # new_user.save()
            user_detail = UserDetail(
                user=new_user,
                mobile_no=data['altMobileNumber'],
                address=data['address'],
                land_mark=data['landMark'],
                address_type=data['addressType'],
                location=data['location'],
                pincode=data['pincode'],
            )
            user_detail.save()
                
        except IntegrityError as e:
            return JsonResponse(
                {
                    'status': 'email id exists'
                }, safe=False, status=200,
            )
        except Exception as e:
            return JsonResponse(
                {
                    'status': 'failed'
                }, safe=False, status=200,
            )
        return JsonResponse({'status': 'success'}, status=200, safe=False)

