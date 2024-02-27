from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from commons.services import STICHING_SERVICES
from commons.user_role import admin_only
from dashboard.services.models import StichingItemRelation


@login_required
@admin_only
def update_sort_order(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        sort_order = request.POST.get('sort_order', "") if request.POST.get('sort_order', '') else  None
        relation = StichingItemRelation.objects.get(id=id)
        category_id = relation.category_id
        finishing_id = relation.finishing_id
        pattern_id = relation.pattern_id
        service_id = relation.service_id
        if sort_order == None:
            relation.sort_order = sort_order
            relation.save()
            return JsonResponse({"status":1})
        else:
            # check_duplicate = StichingItemRelation.objects.filter(category_id=category_id,finishing_id=finishing_id,
            # pattern_id=pattern_id, service_id=service_id,sort_order=sort_order).exists()
            # if check_duplicate:
            #     return JsonResponse({"status": 0})
            # else :
            relation.sort_order = sort_order
            relation.save()
            return JsonResponse({"status":1})
            
    else:
        return JsonResponse({"status": 0})
