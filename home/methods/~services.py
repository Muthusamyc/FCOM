import json
from django.shortcuts import render
from dashboard.services.models import (
    StichingCategory,
    StichingService,
    StichingFinish,
    StichingPattern
)
__services = {'category' : StichingCategory,
            'service' : StichingService,
            'finishing' : StichingFinish,
             'pattern' : StichingPattern
            }
# Create your views here.
def services(request):
    data = {}
    for service_name, service_obj in __services.items():
        data[service_name] = service_obj.objects.all().values('id', 'name')

    for key, val in data.items():
        print(key, val)
    return render(request, "services.html", {'services' : data})
