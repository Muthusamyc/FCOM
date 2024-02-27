import requests
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from dashboard.services.models import Cart, ItemsInCart
import logging
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_cart_to_user_browser(request):
    if request.user.is_authenticated:
        check_cart = Cart.objects.filter(user_id=request.user.id, status=1).exists()
        if check_cart:
            saved_cart = Cart.objects.get(user_id=request.user.id, status=1)
            items_in_cart = ItemsInCart.objects.filter(cart_id=saved_cart.id)
            
            itemsInCart = {}
            itemsInCart['item'] = []
            for item in items_in_cart:
                itemsInCart['item'].append({
                    item.id : {
                        'qty' : item.qty,
                        'sub_total' : item.sub_total
                    }
                })
            itemsInCart['estimatedTotal'] = saved_cart.estimated_price
            itemsInCart['totalItems'] = saved_cart.total_items
            itemsInCart['advancePayable'] = saved_cart.advance_payable
            
            return JsonResponse({
                'message' : itemsInCart
            }, status=200, safe=False)
            

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def remove_item_from_cart(request):
    try:            
       data = request.data
       cart_id = data['cartId']
       item_id = data['itemId']
      
       items_in_cart = request.COOKIES.get('itemsInCart')
       items_in_cart = json.loads(items_in_cart)
       
       estimated_price = items_in_cart['estimatedTotal']
       total_items = items_in_cart['totalItems']
       advance_payable = items_in_cart['advancePayable']
       
       cart = Cart.objects.get(id=cart_id)
       item = ItemsInCart.objects.get(cart_id=cart_id, item_id=item_id)
       
       if total_items == 0:
           item.delete()
           cart.delete()
           return JsonResponse({'status' : 'ok'})       
       
       cart.estimated_price = estimated_price
       cart.total_items = total_items
       cart.advance_payable = advance_payable
       cart.save()
       try:            
           item_in_cart = items_in_cart['items'][item_id]
           item.qty = item_in_cart['qty']
           item.sub_total = item_in_cart['sub_total']
           item.save()        
       except KeyError as e:
           item.delete()           
       return JsonResponse({'status' : 'ok'})       
    except Exception as e:
        
        logging.error(str(e))
        return JsonResponse(
            {'status' : 'failed'},
            status=status.HTTP_400_BAD_REQUEST
        )
