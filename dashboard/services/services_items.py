from .models import StichingItem, StichingItemRelation
from commons.user_role import admin_only
from commons.services import STICHING_SERVICES
from commons.logging import api_error_logger, request_error_logger
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
import logging

from commons.logging import api_error_logger, request_error_logger
from commons.services import STICHING_SERVICES
from commons.user_role import admin_only


ITEMS_PER_PAGE = 40


@login_required
@admin_only
@request_error_logger
def add(request):

    all_services = {}
    for service_name, service_obj in STICHING_SERVICES.items():
        all_services[service_name] = service_obj.objects.all().values(
            'id', 'name')
    if request.method == "POST":
        category_id = request.POST.get('Category', '')
        service_id = request.POST.get('Service', '')
        finishing_id = request.POST.get('Finishing', '')
        pattern_id = request.POST.get('Pattern', '')

        item_name = request.POST.get('name', '')
        starting_price = request.POST.get('startingPrice', '').strip()
        estimated_price = request.POST.get('estimatedPrice', '').strip()
        item_image = request.FILES.get('itemImage', '')
        tags = request.POST.get('tags', '')

        new_item = StichingItem(
            name=item_name,
            starting_price=starting_price,
            estimated_price=estimated_price,
            tags=tags,
            image=item_image,
        )
        new_item.save()

        new_relation = StichingItemRelation(
            category_id=category_id,
            service_id=service_id,
            finishing_id=finishing_id,
            pattern_id=pattern_id,
            item_id=new_item.id,
        )
        new_relation.save()
        messages.info(request, "Item saved successfully")
        return redirect(add)
    return render(request, 'products/add.html', {'services': all_services})


@login_required
@admin_only
@request_error_logger
def edit(request, id):
    all_services = {}
    for service_name, service_obj in STICHING_SERVICES.items():
        all_services[service_name] = service_obj.objects.all().values(
            'id', 'name')
    relation = StichingItemRelation.objects.get(id=id)
    item = StichingItem.objects.get(id=relation.item_id)
    if request.method == "POST":
        category_id = request.POST.get('Category', '')
        service_id = request.POST.get('Service', '')
        finishing_id = request.POST.get('Finishing', '')
        pattern_id = request.POST.get('Pattern', '')
        priority_id = request.POST.get('Priority', '')

        item_name = request.POST.get('name', '')
        starting_price = request.POST.get('startingPrice', '')
        estimated_price = request.POST.get('estimatedPrice', '')
        item_image = request.FILES.get('itemImage', '')
        tags = request.POST.get('tags', '')
        item_type_id = request.POST.get('ItemType', '')

        item.name = item_name
        item.starting_price = starting_price
        item.estimated_price = estimated_price
        item.image = item_image if item_image else item.image
        item.tags = tags
        item.save()

        relation.category_id = category_id
        relation.service_id = service_id
        relation.finishing_id = finishing_id
        relation.pattern_id = pattern_id
        relation.priority = priority_id
        relation.item_id = item.id
        relation.item_type = item_type_id
        relation.save()

        return redirect(list)

    return render(request, "products/edit.html", {'services': all_services, 'relation': relation})


@login_required
@admin_only
@request_error_logger
def list(request):
    page_no = request.GET.get('page', 1)
    all_services = {}
    for service_name, service_obj in STICHING_SERVICES.items():
        all_services[service_name] = service_obj.objects.all().values(
            'id', 'name')
    all_items = StichingItemRelation.objects.filter(
        status=1).all().order_by('-id')

    paginated_items = Paginator(all_items, ITEMS_PER_PAGE)
    try:
        paginated_items = paginated_items.page(page_no)
    except PageNotAnInteger:
        paginated_items = paginated_items.page(1)
    except EmptyPage:
        paginated_items = paginated_items.page(paginated_items.num_pages)
    return render(request, 'products/list.html', {'services': all_services, 'all_items': paginated_items})


@login_required
@admin_only
@request_error_logger
def filter(request):
    page_no = request.GET.get('page', 1)
    all_services = {}
    for service_name, service_obj in STICHING_SERVICES.items():
        all_services[service_name] = service_obj.objects.all().values(
            'id', 'name')

    list_of_items = []
    if request.method == "POST":
        all_items = StichingItemRelation.objects.filter(
            status=1).all().order_by('sort_order')
        finishing_id = request.POST.get('finishing', '').strip()
        category_id = request.POST.get('category', '').strip()
        service_id = request.POST.get('service', '').strip()
        pattern_id = request.POST.get('pattern', '').strip()
        filter_values = [category_id, finishing_id, service_id, pattern_id]
        if finishing_id:
            all_items = all_items.filter(finishing_id=finishing_id)
        if category_id:
            all_items = all_items.filter(category_id=category_id)
        if service_id:
            all_items = all_items.filter(service_id=service_id)
        if pattern_id:
            all_items = all_items.filter(pattern_id=pattern_id)
        all_items = all_items.order_by('sort_order')

        items_per_page = Paginator(all_items, ITEMS_PER_PAGE)
        try:
            list_of_items = items_per_page.page(page_no)
        except PageNotAnInteger:
            list_of_items = items_per_page.page(1)
        except EmptyPage:
            list_of_items = items_per_page.page(items_per_page.num_pages)
        return render(request, 'products/filtered.html', {'services': all_services, 'all_items': list_of_items, 'filter_values': filter_values})

    return render(request, 'products/filtered.html', {'services': all_services, 'all_items': list_of_items})


@login_required
@admin_only
@api_error_logger
def delete(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item = StichingItemRelation.objects.get(id=item_id)
        item.status = 0
        item.save()
        return JsonResponse({"status": 1})


@login_required
@admin_only
@request_error_logger
def view_edit_order(request):
    all_services = {}
    for service_name, service_obj in STICHING_SERVICES.items():
        all_services[service_name] = service_obj.objects.all().values(
            'id', 'name')

    if request.method == 'POST':
        id = request.POST.get('item_id')
        category_val = request.POST.get('category_val', '')
        finishing_val = request.POST.get('finishing_val', '')
        service_val = request.POST.get('service_val', '')
        pattern_val = request.POST.get('pattern_val', '')
        relation = StichingItemRelation.objects.get(id=id)
        return render(request, "products/filter_page_edit.html", {'services': all_services, 'relation': relation,
                                                                  'category_val': category_val, 'finishing_val': finishing_val,
                                                                  'service_val': service_val, 'pattern_val': pattern_val})


@request_error_logger
@login_required
@admin_only
def edit_filtered_items(request, id):

    page_no = request.GET.get('page', 1)
    all_services = {}
    for service_name, service_obj in STICHING_SERVICES.items():
        all_services[service_name] = service_obj.objects.all().values(
            'id', 'name')
    list_of_items = []

    relation = StichingItemRelation.objects.get(id=id)
    item = StichingItem.objects.get(id=relation.item_id)
    if request.method == "POST":
        category_id = request.POST.get('Category', '')
        service_id = request.POST.get('Service', '')
        finishing_id = request.POST.get('Finishing', '')
        pattern_id = request.POST.get('Pattern', '')
        priority_id = request.POST.get('Priority', '')
        item_name = request.POST.get('name', '')
        starting_price = request.POST.get('startingPrice', '')
        estimated_price = request.POST.get('estimatedPrice', '')
        item_image = request.FILES.get('itemImage', '')
        tags = request.POST.get('tags', '')
        item_type_id = request.POST.get('ItemType', '')
        item.name = item_name
        item.starting_price = starting_price
        item.estimated_price = estimated_price
        item.image = item_image if item_image else item.image
        item.tags = tags
        item.save()
        relation.category_id = category_id
        relation.service_id = service_id
        relation.finishing_id = finishing_id
        relation.pattern_id = pattern_id
        relation.priority = priority_id
        relation.item_id = item.id
        relation.item_type = item_type_id
        relation.save()
        all_items = StichingItemRelation.objects.filter(
            status=1).all().order_by('sort_order')
        finishing_id = request.POST.get('finishing_val', '')
        category_id = request.POST.get('category_val', '')
        service_id = request.POST.get('service_val', '')
        pattern_id = request.POST.get('pattern_val', '')
        filter_values = [category_id, finishing_id, service_id, pattern_id]
        if finishing_id:
            all_items = all_items.filter(finishing_id=finishing_id)
        if category_id:
            all_items = all_items.filter(category_id=category_id)
        if service_id:
            all_items = all_items.filter(service_id=service_id)
        if pattern_id:
            all_items = all_items.filter(pattern_id=pattern_id)
        all_items = all_items.order_by('sort_order')
        items_per_page = Paginator(all_items, ITEMS_PER_PAGE)
        try:
            list_of_items = items_per_page.page(page_no)
        except PageNotAnInteger:
            list_of_items = items_per_page.page(1)
        except EmptyPage:
            list_of_items = items_per_page.page(items_per_page.num_pages)
        return render(request, 'products/filtered.html', {'services': all_services, 'all_items': list_of_items, 'filter_values': filter_values})
