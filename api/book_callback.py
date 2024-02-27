from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from home.models import BookCallBack

from .serializers import BookCallBackSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def book_callback(request):
    """
        Book a appointment with fcom and return the appointment id
    """
    try:

        if request.method == 'POST':
            data = request.data
            callback_serializer = BookCallBackSerializer(data=data)
            if callback_serializer.is_valid():
                callbackmsg = callback_serializer.save()
                ticket = BookCallBack.objects.get(id=callbackmsg.id)
                ticket.ticketid = f'Ticketid{str(callbackmsg.id).zfill(5)}'
                ticket.save()
                return JsonResponse({'status': 'success'}, safe=False)
            return JsonResponse(callback_serializer.errors, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
