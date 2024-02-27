
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from dashboard.services.models import (StichingCategory, StichingFinish,
                                       StichingPattern, StichingService)
from commons.services import STICHING_SERVICES, get_service_class

from home.models import PartnerForm
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def partners_services(request):
    """
        Book a appointment with fcom and return the appointment id
    """
    try:
        if request.method == "GET":
            all_services = {}
            for service_name, service_obj in STICHING_SERVICES.items():
                all_services[service_name] = list( service_obj.objects.all().values('id', 'name'))

            return JsonResponse({'all_services' : all_services}, status=200)
            
        if request.method == 'POST':
            data = request.data
            partner = PartnerForm(
                full_name = data['fullName'],
                email = data['email'],
                mobile_no = data['mobileNumber'],
                service_type = data['servicesTypePartnerForm'],
                service_name = data['servicesPartnerForm'],
                organization_name = data['organization'],
                
            )
            partner.save()                        
            return JsonResponse({'status': 'success'}, safe=False)
            
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
