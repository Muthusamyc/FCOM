from django.db import models

from home.models import *
from dashboard.master.models import User

# class Service(models.Model):
#     service_name = models.CharField(max_length=200)
#     service_description = models.CharField(max_length=2000)
#     gender = models.CharField(max_length=1)
#     created_by = models.CharField(max_length=1)
#     created_date = models.DateTimeField(null=True)
#     modified_by = models.CharField(max_length=1)
#     modified_date = models.DateTimeField(null=True)
 

 
# Create your models here.
class BookCallBack(models.Model):
    mobile_no = models.CharField(max_length=50, null=True)
    note = models.CharField(max_length=500, null=True)
    ticketid = models.CharField(max_length=50, null=True)
    feedback = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(default=0, null=True)
    
class PartnerForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    service_type = models.CharField(max_length=100, null=True)
    service_name = models.CharField(max_length=100, null=True)
    organization_name = models.CharField(max_length=500, null=True)
    
