from django.urls import path


from .views import (
    index,
    listings,
    callbacks_update,
    follow_up,
    partners_forms,
    search_order
)

urlpatterns = [
    path('dashboard', index, name="dashboard"),
    path('callbacks', listings, name="callback_listings"),
    path('callbacks/update/<int:id>', callbacks_update, name="callback_update"),
    path('partner-forms', partners_forms, name="partner_form_listings"),
    path('followup', follow_up, name="followup_listings"),
    path('search-page', search_order, name="search_order"),

]
