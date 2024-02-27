import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from commons.logging import api_error_logger
from dashboard.services.models import Cart, ItemsInCart, StichingItemRelation



@cache_page(60*60*2)
@api_view(['POST'])
@permission_classes([AllowAny])
@api_error_logger
def get_service_items(request):
    if request.method == "POST":

        data = request.data
        services = json.loads(data['data'])

        first_page_items = StichingItemRelation.objects.filter(
            category_id=services['category'],
            service_id=services['service'],
            pattern_id=services['pattern'],
            finishing_id=services['finishing'],
            status=1
        ).all().values('id', 'item__name', 'item__starting_price', 'item__estimated_price', 'item__image',  'item__tags')

        first_page_items = first_page_items.order_by('sort_order')
        item_counts = first_page_items.count()
        first_page_items = list(first_page_items)

        check_cart = Cart.objects.filter(
            user_id=request.user.id, status=1).exists()
        itemsInCart = {}
        if check_cart:
            saved_cart = Cart.objects.get(user_id=request.user.id, status=1)
            items_in_cart = ItemsInCart.objects.filter(cart_id=saved_cart.id)

            itemsInCart = {}
            itemsInCart['items'] = {}
            for item in items_in_cart:
                itemsInCart['items'].update({
                    str(item.item.id): {
                        'qty': item.qty,
                        'sub_total': item.sub_total
                    }
                })
            itemsInCart['estimatedTotal'] = saved_cart.estimated_price
            itemsInCart['totalItems'] = saved_cart.total_items
            itemsInCart['advancePayable'] = saved_cart.advance_payable
   
        return JsonResponse({
            'message': 'ok',
            'first_page_items': first_page_items,
            'item_counts': item_counts,
            'itemsInCart': itemsInCart

        }, status=200, safe=False)


@cache_page(60*60*2)
@api_view(['POST'])
@permission_classes([AllowAny])
def get_service_items_from_desinger(request):
    if request.method == "POST":

        data = request.data
        services = json.loads(data['data'])

        first_page_items = StichingItemRelation.objects.filter(
            category_id=services['category'],
            service_id=services['service'],
            pattern_id=services['pattern'],
            finishing_id=services['finishing'],
            item_type=2
        ).all().values('id', 'item__name', 'item__starting_price', 'item__estimated_price', 'item__image',  'item__tags')

        item_counts = first_page_items.count()
        first_page_items = list(first_page_items)

        # page_no, limit = data['page'], data['limit']
        # paginator = Paginator(first_page_items, limit)

        # page_items_data = []
        # try:
        #     page_items_data += paginator.page(page_no).object_list
        # except PageNotAnInteger:
        #     page_items_data += paginator.page(1).object_list
        # except EmptyPage:
        #     page_items_data = []
        return JsonResponse({
            'message': 'ok',
            'first_page_items': first_page_items,
            'item_counts': item_counts

        }, status=200, safe=False)


@cache_page(60*60*2)
@api_view(['POST'])
@permission_classes([AllowAny])
def get_service_search_items(request):
    if request.method == "POST":

        search_text = request.POST.get('data', '')

        first_page_items = StichingItemRelation.objects.filter(item__name__icontains=search_text,status=1).all().values(
            'id', 'item__name', 'item__starting_price', 'item__estimated_price', 'item__image',  'item__tags')

        first_page_items = first_page_items.order_by('sort_order')
        item_counts = first_page_items.count()
        first_page_items = list(first_page_items)

        check_cart = Cart.objects.filter(
            user_id=request.user.id, status=1).exists()
        itemsInCart = {}
        if check_cart:
            saved_cart = Cart.objects.get(user_id=request.user.id, status=1)
            items_in_cart = ItemsInCart.objects.filter(cart_id=saved_cart.id)

            itemsInCart = {}
            itemsInCart['items'] = {}
            for item in items_in_cart:
                itemsInCart['items'].update({
                    str(item.item.id): {
                        'qty': item.qty,
                        'sub_total': item.sub_total
                    }
                })
            itemsInCart['estimatedTotal'] = saved_cart.estimated_price
            itemsInCart['totalItems'] = saved_cart.total_items
            itemsInCart['advancePayable'] = saved_cart.advance_payable

        # page_no, limit = data['page'], data['limit']
        # paginator = Paginator(first_page_items, limit)

        # page_items_data = []
        # try:
        #     page_items_data += paginator.page(page_no).object_list
        # except PageNotAnInteger:
        #     page_items_data += paginator.page(1).object_list
        # except EmptyPage:
        #     page_items_data = []
        return JsonResponse({
            'message': 'ok',
            'first_page_items': first_page_items,
            'item_counts': item_counts,
            'itemsInCart': itemsInCart

        }, status=200, safe=False)
