from datetime import datetime
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from commons.services import STICHING_SERVICES
from dashboard.services.models import (Cart, ItemsInCart, Order,
                                       OrderTracking, StichingItem,
                                       StichingItemRelation,
                                       TransactionDetails)

from commons.booking_stages import BookingStage, STAGES
from ..helpers import update_order_status

def add_item_to_order(request):    
        
    if request.method == "POST":
        designer_updated_price = request.POST.get('designer_updated_price', '')
        item = request.POST.get('item', '')
        pass
        
    return redirect("order_details")

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_item_price_by_designer(request):    
    if request.method == "POST":
        cart_id = request.POST.get('cartId')
        new_item_price_by_designer = request.POST.get('newItemPriceForOrder')
        order = ItemsInCart.objects.get(cart_id=cart_id)
        order.designer_updated_price = new_item_price_by_designer 
        order.save()
        
        return JsonResponse({
            'status' : 'success'
        }, status=200, safe=False)   


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_status_with_date(request):
    if request.method == "POST":       
        order_id = request.POST.get('orderId', '')
        date_type = request.POST.get('dateType')
        date = request.POST.get('date')
        order = Order.objects.get(id=order_id)
        date = datetime.strptime(date, '%d-%m-%Y')

        ORDER_STATUS = None
        if date_type == "Pick Up":
            order.pickup_date = date
            ORDER_STATUS = BookingStage.ORDER_PICKEDUP
        if date_type == "Visit/Consultation":
            order.consultation_date = date
            ORDER_STATUS = BookingStage.ORDER_CONSULTED
        if date_type == "Delivery":
            order.delivery_date = date
            ORDER_STATUS = BookingStage.ORDER_DELIVERED
        if date_type == "InProgress":
            order.inprogress_date = date
            ORDER_STATUS = BookingStage.ORDER_IN_PROGRESS
        try:            
            order.save()
            
            update_order_status(order_id, ORDER_STATUS)
            
            order_tracker = OrderTracking.objects.filter(
                    order_id=order_id, status=ORDER_STATUS).last()
    
            if order_tracker:
                order_tracker.created_on = datetime.now()
                order_tracker.save()
            else:
                new_order_tracker_entry = OrderTracking()
                new_order_tracker_entry.status = ORDER_STATUS
                new_order_tracker_entry.status_name = STAGES[ORDER_STATUS]
                new_order_tracker_entry.created_on = datetime.now()
                new_order_tracker_entry.order_id = order_id
                new_order_tracker_entry.save()
            return JsonResponse({
                'status' : '1'
                }, status=200, safe=False)   

        except Exception as e:
            print(e)
            return JsonResponse({
                'status' : '0'
                }, status=200, safe=False)   