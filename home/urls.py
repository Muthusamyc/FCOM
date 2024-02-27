from django.urls import path
from home.methods.cart import cart
from .views import *
from .api import partners_services, send_login_otp, verify_otp, send_signup_otp, verify_singup_otp, set_singup_password, signup_add_details

from .methods.paytm import paytm_callback

urlpatterns = [
    path('our-story', our_story, name="our_story"),
    path('our-work', our_work, name="our_work"),
    path('cancelation-refund', policy_cancelation_refund, name="policy_cancelation_refund"),
    path('terms-&-conditions', terms_and_conditions, name="terms_and_conditions"),
    path('my-profile', my_profile, name="my_profile"),
    path('services', our_services, name="our_services"),
  #  path('cart', cart, name="cart"),
    path('faqs', faqs, name="faqs"),
    path('book-now', book_now, name="book_now"),
    path('thank-you', thank_you, name="thank_you"),
    path('fabric-care', fabric_care, name="fabric_care"),
    #path('blogs', blogs, name="blogs"),
#    path('my-booking', my_booking, name="my_booking"),
    #path('my-booking-items', my_booking_items, name="my_booking_items"),
    path('paytm-callback', paytm_callback, name="paytm_callback_old"),
    path('partner-services', partners_services, name="partners_services"),
    
    path('send-opt', send_login_otp, name="send_otp"),
    path('verfify-otp', verify_otp, name="verify_otp"),
   
    path('contact',  contact, name="contact"),
    path('signup-with-otp', send_signup_otp, name="send_signup_otp"),
    path('verify-signup-otp', verify_singup_otp, name="verify_otp"),
    path('signup-create-password', set_singup_password, name="set_singup_password"),
    path('signup-add-details', signup_add_details, name="signup_add_details"),
    path('partner-profile', partner_profile, name='partner_profile'),
    path('add-family-members', add_family_members, name='add_family_members'),
    path('edit_family_members/<int:id>', edit_family_members, name='edit_family_members'),
    path('add-address-book', add_address_book, name='add_address_book'),
    path('edit-address-book/<int:id>', edit_address_book, name='edit_address_book'),
    
    
]