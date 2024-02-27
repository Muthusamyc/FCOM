from django.urls import path

from dashboard.master import views
from .views import (add_user, delete_user, edit_partner, edit_user, list_user,
                    selected_users, partner_my_work, customer_report, order_report, 
                    amount_collected, report_orders_listing, top_sales, designer_reviews, 
                    designer_performance, order_movement_report, designer_sales,partner_gallery, remove_gallery)


urlpatterns = [
    path('add-user', add_user, name="add_user"),
    path('list-of-users', list_user, name="list_user"),
    path('selected-users/<str:role>/', selected_users, name="selected_users"),
    path('edit-users/<int:id>/', edit_user, name="edit_user"),
    path('edit-partner/', edit_partner, name="edit_partner"),
    path('delete/<int:id>/', delete_user, name='delete_user'),
    path('customer-report', customer_report, name="customer_report"),
    path('order-report', order_report, name="order_report"),
    path('designer-sales', designer_sales, name="designer_sales"),
    path('designer-performance', designer_performance, name="designer_performance"),
    path('amount-collected', amount_collected, name="amount_collected"),
    path('report-orders-listing/<str:status>', report_orders_listing, name="report_orders_listing"),
    path('top-sales', top_sales, name="top_sales"),
    path('designer-reviews', designer_reviews, name="designer_reviews"),
    path('order-movement', order_movement_report, name='order_movement_report'),
    path('partner-my-work', partner_my_work, name='partner_my_work'),
    path('parter-gallery', partner_gallery, name='partner_gallery'),
    path('remove-image/<int:id>/',remove_gallery, name="remove_gallery")
    
    
]
