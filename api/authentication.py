
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import SignUpDetail, SignUpUser


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
        This method is to signup new users from the client side application
    """
    if request.method == 'POST':
        data = request.data
        try:
            new_user = SignUpUser.objects.create_user(
                data['email'], data['email'], data['signUpPassword'])
            new_user.last_name = data['lastName']
            new_user.first_name = data['firstName']
            new_user.role = data['userType']
            #new_user.username = data['email']
            new_user.mobile_no = data['mobileNumber']
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
                user=new_user,
                mobile_no=data['mobileNumber'],
                address=data['address'],
                land_mark=data['landMark'],
                address_type=data['addressType'],
                location=data['location'],
                pincode=data['pincode'],
            )
            user_detail.save()
        except IntegrityError as e:
            return JsonResponse(
                {
                    'message': 'email id exists'
                }, safe=False, status=200,
            )
        except Exception as e:
            print(e)
        return JsonResponse({'message': 'ok'}, status=200, safe=False)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    try:
        data = request.data
        user = authenticate(
            request=request, email=data['userId'], password=data['password'])
        if user:
            login(request=request, user=user)
            return JsonResponse(
                {
                    'message': 'loggedin'
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
                'message': "something went wrong!"
            },
            status=400, safe=False
        )


@login_required
@permission_classes([IsAuthenticated])
def sign_out(request):
    logout(request=request)
    return redirect("HomePage")


@api_view(['GET'])
@permission_classes([AllowAny])
def is_user_authenticated(request):
    is_authenticated = request.user.is_authenticated
    return JsonResponse({
        'message': is_authenticated
    }, safe=False)
