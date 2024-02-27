from django.db import models
from dashboard.master.models import User
from django.contrib.humanize.templatetags import humanize

from fcom import settings
 
class Messages(models.Model):

    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    message_type = models.CharField(max_length=50, default="text", null=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    uploaded_file = models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return self.message
    
    def get_date(self):
        return humanize.naturaltime(self.timestamp)
