from django.db import models

# Create your models here.

class Seometadata(models.Model):
    page = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=50, null=True)
    keywords = models.CharField(max_length=50, null=True)
    created_on = models.DateTimeField(auto_now_add=True)