from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from commons.user_role import authenticated_user,allowed_users,admin_only

from .models import Seometadata

import json

# Create your views here.

def writ_to_json(meta_data):
        json_meta = json.load(open('data/meta_data.json'))
        if meta_data.page in json_meta['page']:
            json_meta["page"][meta_data.page]['title'] = meta_data.title
            json_meta["page"][meta_data.page]['keywords'] = meta_data.keywords
            json_meta["page"][meta_data.page]['description'] = meta_data.description
            json.dump(json_meta, open('data/meta_data.json', 'w'), indent=4)
        else:
            meta_data = {meta_data.page:
                {'title': meta_data.title,
                   'keywords': meta_data.keywords,
                   'description': meta_data.description}}
            json_meta["page"].update(meta_data)
            json.dump(json_meta, open('data/meta_data.json', 'w'), indent=4)
 
# the result is a JSON string:


@login_required
@admin_only
def create_seo(request):
    seodata = Seometadata.objects.all().order_by('-id')[:4]
    if request.method == "POST":
        page = request.POST['page']
        title = request.POST['title']
        keywords = request.POST['keywords']
        description = request.POST['description']
        meta_data = Seometadata(
            page=page,
            title=title,
            description=description,
            keywords=keywords
        )
        meta_data.save()
        writ_to_json(meta_data)
        seodata = Seometadata.objects.all().order_by('-id')[:5]
        return render(request, 'add_seo.html',{'seodata':seodata})
    return render(request, 'add_seo.html',{'seodata':seodata})

@login_required
@admin_only
def list_seo(request):
    seodata = Seometadata.objects.all().order_by('-id')
    return render(request, 'list_seo.html',{'seodata':seodata})

@login_required
@admin_only
def edit_seo(request,id):
    seodata = Seometadata.objects.get(id=id)
    if request.method == "POST":
        seodata.page = request.POST['page']
        seodata.title = request.POST['title']
        seodata.keywords = request.POST['keywords']
        seodata.description = request.POST['description']
        seodata.save()
        writ_to_json(seodata)
        return redirect(list_seo)
    return render(request, 'edit_seo.html',{'seodata':seodata})



