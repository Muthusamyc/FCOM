import requests
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt

from dashboard.services.models import Order, PayTMTransactionDetails
from payment_gateway.paytm import config, PaytmChecksum


import logging

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_order(request):
    data = request.data
    cart_id = data['cartId']
    payment_type = data['paymentType']
    amount = data['amount']
    
    main_order = Order(
        cart_id = cart_id,
        made_by = request.user,    
        payment_type = payment_type,
        payment_amount = amount, 
        status = "Initiated"
    )
    main_order.save()   
    
    token = config.getTransactionToken(str(main_order.id), amount=amount, customer_id=request.user.id)
    return JsonResponse(
        {
            'orderId' : main_order.id,
            'token' : token,
            'amount' : amount
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def cancel_order(request):
    data = request.data
    order = Order.objects.get(id=data['orderId'])
    order.status = "Canceled"
    order.save()
    return JsonResponse(
        {
            'orderId' : order.id,
            'status' : "Canceled"         
            
        })


    # advanceAmount = data['advanceAmount'].strip()    
    # advance_amt_order = PayTMTransactionDetails(
    #     order_id = main_order.id,        
    #     payment_type = "advance",
    #     payment_amount = advanceAmount,        
    # )
    # advance_amt_order.save()    
    # advanceToken = config.getTransactionToken(str(advance_amt_order.id), amount=advanceAmount, customer_id=request.user.id)
    
    # if advanceToken == '':
    #     logging.ERROR(f"Token intialization failed for id {advance_amt_order.id} / {advanceAmount}")
       
        
    # estimatedAmount = data['estimatedAmount'].strip()
    # estimated_amt_order =  PayTMTransactionDetails(
    #     order_id=main_order.id,
    #     payment_type = "estimated",
    #     payment_amount = estimatedAmount,
    # )
    # estimated_amt_order.save()
    # estimatedToken = config.getTransactionToken(str(estimated_amt_order.id), amount=estimatedAmount, customer_id=request.user.id)
    
    
    # return JsonResponse({
    #     'mainOrderId' : main_order.id,
    #     'advance' : { 'amount' : advanceAmount, 'token' : advanceToken, 'orderId' : str(advance_amt_order.id) },
    #     'estimated' : { 'amount' : estimatedAmount, 'token' : estimatedToken, 'orderId' : str(estimated_amt_order.id) },
        
    # }, status=200, safe=False)
    
    