
from django.urls.conf import path
from .views import (orders_listing, order_listing_for_designer, 
                    order_details, add_item_to_order, update_order_item_price_by_designer,add_extra_material_to_order,
                    assign_order_designer,
                    update_order_service_date_for_order, update_delivery_date, update_order_status_by_deisnger,
                    send_approval_request,order_pickedup, update_canceled_stages, add_measurements, master_measurements,
                    upload_picked_image
                    )

from .api.orders import update_order_status_with_date
#from .api.orders import update_order_item_price_by_designer

urlpatterns = [
    path('listing/<int:id>', orders_listing, name="orders_listing"),
    path('order-lisnting/<int:order_status>', order_listing_for_designer, name="orders_listing_for_designer"),
    path('picked-up', order_pickedup, name="order_pickedup"),
    path('details/<int:id>', order_details, name="order_details"),
    path('add-new-item-to-order/', add_item_to_order, name="add_item_to_order"),
    path('add-new-extra-material-to-order/', add_extra_material_to_order, name="add_extra_material_to_order"),
    path('update-item-price/', update_order_item_price_by_designer, name="update_item_price"),
    path('assignee-designer/', assign_order_designer, name="assign_order_designer"),
    path('update-order-date/<int:id>', update_order_service_date_for_order, name="update_order_service_date_for_order"),
    path('update-canceled_stages/<int:id>', update_canceled_stages, name="update_canceled_stages"),
    path('update-delivery-date/', update_delivery_date, name="update_delivery_date"),
    path('update-order-status/', update_order_status_by_deisnger, name="update_order_status_by_deisnger"),
    path('send-approval-request/', send_approval_request, name='send_approval_request'),
    path('update-date-with-status/', update_order_status_with_date, name='update_order_status_with_date'),
    path('master-measurements/<int:id>', master_measurements, name="master_measurements"),
    path('add-measurements', add_measurements, name="add_measurements"),
    path('upload-picked-image', upload_picked_image, name="upload_picked_image"),
    
]

