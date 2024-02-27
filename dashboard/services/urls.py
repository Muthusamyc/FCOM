from django.urls import path
from . import custom_stiching_services as stiching_services
from . import  services_items 
from . import preferences
from . import measurement_groups
from .api.sort import update_sort_order
# from .  import services as services_page
# from .  import catalogue as catalogue_page
# from .  import catalogue_items as item_page

urlpatterns = [
    path('custom-stitiching-categories/<str:page>', stiching_services.add, name="add_stiching_categories"),
    path('custom-stitiching-edit/<str:page>/<int:id>', stiching_services.edit, name="edit_stiching_categories"),
    path('custom-stitiching-delete/<str:page>/<int:id>', stiching_services.delete, name="delete_stiching_categories"),
    path('add-stiching-service', services_items.add, name="add_stiching_items"),
    path('view-stiching-service', services_items.list, name="view_stiching_items"),
    path('view-selected-stiching-service', services_items.filter, name="view_selected_stiching_items"),
    path('view-edit-order', services_items.view_edit_order, name="view_edit_order"),
    path('update-sort-order', update_sort_order, name="update_sort_order"),
    path('add-stiching-service/<int:id>', services_items.edit, name="edit_stiching_items"),
    path('delete-stiching-service/', services_items.delete, name="delete_stiching_items"),
    path('add-order-preference/<str:page>', preferences.add, name="add_preferences"),
    path('edit-order-preference/<str:page>/<int:id>', preferences.edit, name="edit_preferences"),
    path('delete-order-preference/<str:page>/<int:id>', preferences.delete, name="delete_preferences"),
    path('add-estimation-dates/', preferences.estimated_consultation_date, name="estimated_consultation_date"),
    path('edit-estimation-dates/<int:id>', preferences.edit_estimated_consultation_date, name="edit_estimated_consultation_date"),
    path('delete-estimation-dates/<int:id>', preferences.delete_estimated_consultation_date, name="delete_estimated_consultation_date"),
    path('add-measurement-groups/', measurement_groups.add, name="add_measurement_groups"),
    path('edit-measurement-groups/<int:id>', measurement_groups.edit, name="edit_measurement_groups"),
    path('delete-measurement-groups/<int:id>', measurement_groups.delete, name="delete_measurement_groups"),
    path('edit-filtered-stiching-items/<int:id>', services_items.edit_filtered_items, name="edit_filtered_stiching_items"),
    
#     path('add-stiching-finishing', service.add, name="add_stiching_finishing"),
#     path('add-stiching-pattern', service.add, name="add_stiching_pattern"),
 ] #+ [
#     path('add-services/', services_page.add, name='add-service'),
#     path('edit-services/<int:id>', services_page.edit, name='edit-service'),
#     path('add-catalogue/', catalogue_page.add, name='add-catalogue'),
#     path('add-catalogue-item/', item_page.add, name='add-catalogue-item'),
# ]