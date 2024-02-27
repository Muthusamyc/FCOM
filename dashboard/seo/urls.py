from django.urls import path
from .views import create_seo, list_seo, edit_seo

urlpatterns = [

    path('create', create_seo, name="create_seo"),
    path('list', list_seo, name="list_seo"),
    path('edit/<int:id>', edit_seo, name="edit_seo"),
]