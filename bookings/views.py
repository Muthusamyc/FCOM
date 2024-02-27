import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from commons.booking_stages import STAGES, BookingStage, BOOKING_STAGES_FOR_USER
from commons.services import get_preference_class
from dashboard.master.models import UserDetail, User
from dashboard.services.models import (Cart, DesignerPreference, ItemsInCart,
                                       Order, ServiceMode, OrderItems,
                                       StichingItemRelation, DesingerAssignedOrders,
                                       TransactionDetails, CustomerReview)
from home.views import home, our_services
from payment_gateway.paytm import config
from commons.user_role import customer_only
from chat.models import Messages
# cart functionalities
# user must be authenticated to reach cart page else ask user to login - working
# on cart page show all items with quantity and estimation calculation and advance pay btn 
# remove items from cart from both browser storage and database and data should be same 

@customer_only
@csrf_exempt
def cart(request):
    cart_page = "cart.html"
    
    is_user_authenticated = request.user.is_authenticated
    if is_user_authenticated:    
        
        if not request.user.is_details_added:
            messages.add_message(request, messages.INFO, "Please update your user profile")            
            return redirect("my_profile")
        
        service_modes = get_preference_class('service').objects.all()
        designer_preferences = get_preference_class("preference").objects.all()
        
        
        
        items_in_cart = request.COOKIES.get('itemsInCart')
        if not items_in_cart:
            return redirect("our_services")        
        items_in_cart = json.loads(items_in_cart)
        if len(items_in_cart) == 0:
            return redirect("our_services")     
            
        
        
        estimated_price = items_in_cart['estimatedTotal']
        total_items = items_in_cart['totalItems']
        advance_payable = items_in_cart['advancePayable']

        user_details = {}
        if request.user.is_details_added:            
            current_user_details = UserDetail.objects.filter(user_id=request.user.id).first()
            
            user_details['fullName'] = request.user.first_name + " " +  request.user.last_name       
            user_details['mobileNo'] = request.user.mobile_no
            
            user_details['address'] = {
                'address' : current_user_details.address,
                'landMark' : current_user_details.land_mark,
                'pincode' : current_user_details.pincode,
                'location' : current_user_details.location,
                'addressType' : ""
            }       
        
        check_cart = Cart.objects.filter(user_id=request.user.id, status=1).exists()
        if check_cart:
            cart_items = []
            cart = Cart.objects.filter(user_id=request.user.id, status=1).get()
            
            for id in items_in_cart['items']:
                is_item_present = ItemsInCart.objects.filter(cart_id=cart.id, item_id=id).exists()
                if is_item_present:   
                    cart_item = ItemsInCart.objects.filter(cart_id=cart.id, item_id=id).get()
                    if cart_item.qty != int(items_in_cart['items'][id]['qty']):
                        cart_item.qty = items_in_cart['items'][id]['qty']
                        cart_item.save()                       
                else:                                        
                    cart_item = ItemsInCart(
                        cart_id = cart.id,
                        item_id = id,
                        qty = items_in_cart['items'][id]['qty'],
                        sub_total = items_in_cart['items'][id]['sub_total']
                    )
                    cart_item.save()
                    
            cart.estimated_price = estimated_price
            cart.total_items = total_items
            cart.advance_payable = advance_payable    
            cart.save()
                
            count_cart_items = ItemsInCart.objects.filter(cart_id=cart.id).count()
            
            if count_cart_items != len(items_in_cart['items']):
                item_ids = list(items_in_cart['items'].keys())
                remove_cart_items = ItemsInCart.objects.filter(cart_id=cart.id).exclude(item__item_id__in=item_ids)
                remove_cart_items.delete()
                    
            if total_items == 0:
                cart.delete()
           
            
            cart_items =ItemsInCart.objects.filter(cart_id=cart.id).order_by('-id').all()
            return render(request,  cart_page, {'items_in_cart': cart_items,
                                                           'saved_cart': cart,
                                                           'user_details': user_details,
                                                           'designer_preferences': designer_preferences,
                                                           'service_modes': service_modes,
                                                           'env' : config.PAYTM_ENVIRONMENT, 
                                                           'mid' : config.PAYTM_MID })
            
            
        
      
        #get address details here
         
        
        
        

        
        
        
        #check_cart = Cart.objects.filter(user_id=request.user.id, status=1).exists()
        
        # if len(check_cart) > 0:
        #     saved_cart = list(check_cart)[0]            
        #     if saved_cart.estimated_price == str(estimated_price):
        #         cart_items = saved_cart.itemsincart_set.all()
        #         return render(request,  cart_page, {'items_in_cart': cart_items,
        #                                                    'saved_cart': saved_cart,
        #                                                    'user_details': user_details,
        #                                                    'designer_preferences': designer_preferences,
        #                                                    'service_modes': service_modes,
        #                                                    'env' : config.PAYTM_ENVIRONMENT, 
        #                                                    'mid' : config.PAYTM_MID })
            
        
        # del items_in_cart['estimatedTotal']
        # del items_in_cart['totalItems']
        # del items_in_cart['advancePayable'], 

        cart = Cart(
            estimated_price=estimated_price,
            total_items = total_items,
            advance_payable = advance_payable,
            status=1,
            user = request.user
        )
        cart.save()

        cart_items = []
        try:
                
            for id in items_in_cart['items']:
                cart_item = ItemsInCart(
                    cart_id = cart.id,
                    item_id = id,
                    qty = items_in_cart['items'][id]['qty'],
                    sub_total = items_in_cart['items'][id]['sub_total']
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

@customer_only
def my_booking(request):
    my_booking_page = "my-booking.html"
    if request.user.is_authenticated:
        if request.method == "POST":
            selected_status = request.POST.get('filterstatus', '')
            all_status = BOOKING_STAGES_FOR_USER
            booking_types = DesignerPreference.objects.all()
            service_types = ServiceMode.objects.all()
            if selected_status == '0':
                status_exclude = [BookingStage.ORDER_INITIATED, 0]
                my_orders = Order.objects.filter(made_by_id=request.user.id).exclude(status__in=status_exclude).order_by('-id')
            else:
                my_orders = Order.objects.filter(made_by_id=request.user.id,status=selected_status).order_by('-id')
            return render(request, my_booking_page, {'orders' : my_orders, 'booking_types' : booking_types, 'service_types' : service_types, "all_status" : all_status, "selected_status" : int(selected_status)})
        else:
            all_status = BOOKING_STAGES_FOR_USER
        
            booking_types = DesignerPreference.objects.all()
            service_types = ServiceMode.objects.all()
        
            status_exclude = [BookingStage.ORDER_INITIATED, 0]
            my_orders = Order.objects.filter(made_by_id=request.user.id).exclude(status__in=status_exclude).order_by('-id')
            return render(request, my_booking_page, {'orders' : my_orders, 'booking_types' : booking_types, 'service_types' : service_types, "all_status" : all_status})
    else:
        return redirect(home)
    
@login_required(login_url="/")
@customer_only
def my_booked_items(request, id):
    order_detail = Order.objects.filter(id=id).exclude(status=BookingStage.ORDER_INITIATED).first()
    try:
        reviews = CustomerReview.objects.get(order_id=id)
    except:
        reviews={}
    
    items_in_cart = OrderItems.objects.filter(order_id=id).all()
    count_cart_item = OrderItems.objects.filter(order_id=id,status=1).count()
    
    # items_for_my_bookings = []
    
    # for item in items_in_cart:
    #     for _ in range(item.qty):
    #         items_for_my_bookings.append(item)
    
    
    
    current_user_details = UserDetail.objects.filter(user_id=request.user.id).last()
   
    user_details = {}
    user_details['fullName'] = request.user.first_name + " " +  request.user.last_name       
    user_details['mobileNo'] = current_user_details.mobile_no
    user_details['id'] = str(request.user.id)
    
    user_details['address'] = {
        'address' : current_user_details.address,
        'landMark' : current_user_details.land_mark,
        'pincode' : current_user_details.pincode,
        'location' : current_user_details.location,
        'addressType' :  "" #current_user_details.address_type.capitalize() if not current_user_details.address_type else ""
    }   
    
    transaction_details = TransactionDetails.objects.filter(order_id=id).last()
    
    message_objs = {}
    assinged_designer={}  
    send_messg = [] 
    if order_detail.designer_assigned:
        assinged_designer = DesingerAssignedOrders.objects.get(order_id=order_detail.id) 
        
        if request.user.id < assinged_designer.designer.id:
            chat_thread_name = "chat_" + str(assinged_designer.designer.id) + "-" + str(request.user.id)
        else:
            chat_thread_name = "chat_" + str(request.user.id) + "-" + str(assinged_designer.designer.id)
            
        #chat_messages = ChatMessages.objects.filter(thread_name=chat_thread_name).all()
        message_objs = Messages.objects.filter(thread_name=chat_thread_name).all()
        # senders = {}
        # send_messg = []
        # user_obj = request.user
        # username = user_obj.first_name + " " + user_obj.last_name
        # for i, mesg in enumerate(message_objs):
        #     user_obj_temp = User.objects.get(id=mesg.sender)
        #     senders[user_obj_temp.id] = f"{username}"
        #     send_messg.append([f"{int(mesg.sender)}", f"{mesg.message}", mesg.timestamp])
    
    
    return render(request,"my-booked-items.html", {'order_detail' : order_detail, 'transaction_details' : transaction_details, 'user_details' : user_details, 
                                                    'items_in_cart' : items_in_cart, 'count_cart_item' : count_cart_item, 'chat_messages' : message_objs, 'assinged_designer' : assinged_designer,'reviews':reviews})


    
    