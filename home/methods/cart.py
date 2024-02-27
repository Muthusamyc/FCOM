import json
from django.shortcuts import render, redirect

from dashboard.services.models import StichingItemRelation, Cart, ItemsInCart
from commons.services import get_preference_class
from commons.booking_stages import BookingStage
from home.views import our_services

from dashboard.master.models import UserDetail
from payment_gateway.paytm import config
import logging

def cart(request):
    cart_page = "cart/cart.html"
    
    is_user_authenticated = request.user.is_authenticated
    if is_user_authenticated:        
        items_in_cart = request.COOKIES.get('itemsInCart')
        if items_in_cart is None:
            return redirect(our_services)
            
        items_in_cart = json.loads(items_in_cart)

        service_modes = get_preference_class('service').objects.all()
        designer_preferences = get_preference_class("preference").objects.all()
        #get address details here
         
        current_user_details = UserDetail.objects.get(user_id=request.user.id)
        
        user_details = {}
        user_details['fullName'] = request.user.first_name + " " +  request.user.last_name       
        user_details['mobileNo'] = current_user_details.mobile_no
        
        user_details['address'] = {
            'address' : current_user_details.address,
            'landMark' : current_user_details.land_mark,
            'pincode' : current_user_details.pincode,
            'location' : current_user_details.location,
            'addressType' : current_user_details.address_type.capitalize()
        }       

        
        estimated_price = items_in_cart['estimatedTotal']
        total_items = items_in_cart['totalItems']
        advance_payable = items_in_cart['advancePayable']
        
        check_cart = Cart.objects.filter(user_id=request.user.id, status=0).order_by('-id')
        if len(check_cart) > 0:
            saved_cart = list(check_cart)[0]            
            if saved_cart.estimated_price == str(estimated_price):
                cart_items = saved_cart.itemsincart_set.all()
                return render(request,  cart_page, {'items_in_cart': cart_items,
                                                           'saved_cart': saved_cart,
                                                           'user_details': user_details,
                                                           'designer_preferences': designer_preferences,
                                                           'service_modes': service_modes,
                                                           'env' : config.PAYTM_ENVIRONMENT, 
                                                           'mid' : config.PAYTM_MID })
            
        
        del items_in_cart['estimatedTotal']
        del items_in_cart['totalItems']
        del items_in_cart['advancePayable'], 

        cart = Cart(
            estimated_price=estimated_price,
            total_items = total_items,
            advance_payable = advance_payable,
            status=BookingStage.CART_CREATED,       
            user = request.user
        )
        cart.save()

        cart_items = []
        try:
                
            for id in items_in_cart:
                cart_item = ItemsInCart(
                    cart_id = cart.id,
                    item_id = id,
                    qty = items_in_cart[id]['qty']
                ) 
                cart_item.save()
                cart_items.append(cart_item)
        except Exception as e:
            logging.info(items_in_cart)
            logging.error(str(e))
            
            
            
        return render(request, cart_page, {'items_in_cart' : cart_items,
                                           'saved_cart' : cart,
                                           'user_details' : user_details,
                                           'designer_preferences' : designer_preferences,
                                           'service_modes' : service_modes,
                                            'env' : config.PAYTM_ENVIRONMENT, 
                                            'mid' : config.PAYTM_MID })
    else:
        return redirect(our_services)