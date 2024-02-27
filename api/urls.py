from django.urls import path

from .authentication import is_user_authenticated, sign_in, sign_out, signup
from .book_callback import book_callback
from .items import get_service_items, get_service_items_from_desinger, get_service_search_items
from .order import create_order
#from .views import book_callback, signup, sign_in, sign_out, get_service_items, is_user_authenticated

urlpatterns = [
    path('book-callback/', book_callback, name="book_now"),
    path('signup/', signup, name="signup"),
    path('signin/', sign_in, name="signin"),
    path('is-autherized/', is_user_authenticated, name="is_user_authenticated"),
    path('signout/', sign_out, name="signout"),

    path('get-items/', get_service_items, name="get_service_items"),
    path('get-items-from-desingers/', get_service_items_from_desinger, name="get_service_items_from_desinger"),
    # path('create-order/', create_order, name="create_order"),
    # path('paytm-token', paytm_token, name="paytm_token"),
    # path('paytm-callback', paytm_callback, name="paytm_callback")    
    path('get-search-items/', get_service_search_items, name="get_service_search_items"),
]  