from django.urls import path

from bookings.api import (approval_accepted_estimation, delivery_confirmed,
                          approval_rejected_estimation, cancel_order,
                          create_order, remove_order_item,  customer_review,
                          paytm_callback, paytm_token, reshedule_visitdate)

from .views import cart, my_booking, my_booked_items

from bookings.api.cart import remove_item_from_cart, add_cart_to_user_browser
from .transaction_towards_order import create_transaction_towards_order, paytm_callback_trasaction_for_order_redirect

from .order import create_order_redirect, paytm_callback_redirect

urlpatterns = [
    path('cart/', cart, name="cart"),
    path('update-cart/', remove_item_from_cart, name="update_cart"),
    path('add-items-to-localstorage/', add_cart_to_user_browser, name="add_cart_to_user_browser"),
    path('create-order/', create_order, name="create_order"),
    path('transaction-order/', create_transaction_towards_order, name="transaction_order"),
    path('cancel-order/', cancel_order, name="cancel_order"),
    path('approve-estimation/', approval_accepted_estimation, name="approve_estimation"),
    path('delivery-confirmed/', delivery_confirmed, name="delivery_confirmed"),
    path('remove-items/', remove_order_item, name="remove_order_item"),
    path('reject-estimation/', approval_rejected_estimation, name="reject_estimation"),
    path('paytm-token', paytm_token, name="paytm_token"),
    path('paytm-callback', paytm_callback, name="paytm_callback") ,
    path('customer-review/', customer_review, name="customer_review"),
    path('reshedule-visit-date/', reshedule_visitdate, name="reshedule_visitdate"),
    
    path('my-bookings/', my_booking, name='my_booking'),
    path('order-history/<int:id>', my_booked_items, name='my_booking_items'),
    
    
    path('create-order-redirect/', create_order_redirect, name='create_order_redirect'),
    path('paytm-callback-redirect/', paytm_callback_redirect, name='paytm_callback_redirect'),
    path('paytm-callback-transaction-redirect/', paytm_callback_trasaction_for_order_redirect, name='paytm_trasaction_callack'),
]  