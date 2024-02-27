import json
from django.shortcuts import render
from dashboard.services.models import (
    StichingCategory,
    StichingService,
    StichingFinish,
    StichingPattern,
    ServiceMode,
    DesignerPreference
)


STICHING_SERVICES = {'category': StichingCategory,
                     'service': StichingService,
                     'finishing': StichingFinish,
                     'pattern': StichingPattern
                     }


STICHING_SERVICE_PREFERENCES = {
    'service' : ServiceMode,
    'preference' : DesignerPreference
}

def get_service_class(page):
    return STICHING_SERVICES[page]

def get_preference_class(page):
    return STICHING_SERVICE_PREFERENCES[page]

SERVICE_ITEM_TYPE = {
    1 : 'Customer' ,
    2 : "Designer"     
}

