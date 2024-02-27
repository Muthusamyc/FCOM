import json
from django.shortcuts import redirect
from django.db.utils import IntegrityError
# Create your views here.
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from .serializers import BookCallBackSerializer, SignUpUser, SignUpDetail

from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from dashboard.services.models import StichingItemRelation

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
        This method is to signup new users from the client side application
    """
    if request.method == 'POST':
        data = request.data
        try:
            new_user = SignUpUser.objects.create_user(data['email'], data['email'], data['signUpPassword'])
            new_user.last_name = data['lastName']
            new_user.first_name = data['firstName']
            new_user.role = data['userType']
            #new_user.username = data['email']

            new_user.save()

            # new_user = SignUpUser(
            #     first_name = data['firstName'],
            #     last_name = data['lastName'],
            #     email = data['email'],
            #     username = data['email'],
            #     password = data['password'],
            #     role = data['userType']
            # )
            # new_user.save()

            user_detail = SignUpDetail(
                user = new_user,
                mobile_no = data['mobileNumber'],
                address=data['address'],
                land_mark = data['landMark'],
                address_type = data['addressType'],
                location = data['location'],
                pincode = data['pincode'],
            )
            user_detail.save()
        except IntegrityError as e:
            return JsonResponse(
                {
                    'message' : 'email id exists'
                }, safe=False, status=200,
            )
        except Exception as e:
            print(e)
        return  JsonResponse({'message' : 'ok'}, status=200, safe=False)

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    try:
        data = request.data
        user = authenticate(request=request, email=data['userId'], password=data['password'])
        if user:
            login(request=request, user=user)
            return JsonResponse(
                {
                    'message' : 'loggedin'
                },
                status=200, safe=False)
        else:
            return JsonResponse(
                {
                    'message': 'loggingFailed'
                },
                status=200, safe=False
            )
    except Exception as e:
        return JsonResponse(
            {
                'message' : "something went wrong!"
            },
            status = 400, safe=False
        )        
    
@login_required
def sign_out(request):    
    logout(request=request)  
    return redirect("HomePage")
    
@api_view(['POST'])
def book_callback(request):
    """
        Book a appointment with fcom and return the appointment id
    """
    try:
            
        if request.method == 'POST':
            data = request.data
            callback_serializer = BookCallBackSerializer(data=data)            
            if callback_serializer.is_valid():
                callback_serializer.save()
                return JsonResponse({'status': 'success'}, safe=False)
            return JsonResponse(callback_serializer.errors, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@cache_page(60*60*2)
@api_view(['POST'])
@permission_classes([AllowAny])
def get_service_items(request):
    if request.method == "POST":
            
        data = request.data

        services = json.loads(data['data'])
        first_page_items = StichingItemRelation.objects.filter(
            category_id = services['category'],
            service_id = services['service'], 
            pattern_id = services['pattern'],
            finishing_id = services['finishing']
        ).all().values('id', 'item__name', 'item__starting_price', 'item__estimated_price', 'item__image',  'item__tags' )
        item_counts = first_page_items.count()
        first_page_items = list(first_page_items)

        page_no, limit = data['page'], data['limit']
        paginator = Paginator(first_page_items, limit)

        page_items_data = []
        try:
            page_items_data += paginator.page(page_no).object_list
        except PageNotAnInteger:
            page_items_data += paginator.page(1).object_list
        except EmptyPage:
            page_items_data =  []
        return JsonResponse({
            'message' : 'ok',
            'first_page_items' : page_items_data,
            'item_counts' : item_counts

        }, status=200, safe=False)


@api_view(['GET'])
@permission_classes([AllowAny])
def is_user_authenticated(request):
    is_authenticated = request.user.is_authenticated
    return JsonResponse({
        'message' : is_authenticated
    }, safe=False)