from django import template
from dashboard.services.models import Measurementslist , Measurement


register = template.Library()




@register.simple_tag
def get_measurement_size(group_id, id, group ):
    try:
        measurement = Measurementslist.objects.get(name_id=group_id, measurement__user_id=id, measurement__group=group, measurement__is_master=1)
        return measurement.size
    except:
        return ""
    
@register.simple_tag
def get_measurement_size_item(group_id, id, group):
    try:
        measurement = Measurementslist.objects.get(name_id=group_id, measurement__item_id=id,  measurement__group=group)
        return measurement.size
    except:
        return ""
    

@register.simple_tag
def special_notes(id, group):
    try:
        measurement = Measurement.objects.get(item_id=id, group=group)
        return measurement.notes
    except:
        return ""

@register.simple_tag
def special_notes_master(id, group):
    try:
        measurement = Measurement.objects.get(user_id=id, group=group, is_master=1)
        return measurement.notes
    except:
        return ""
    
@register.simple_tag
def check_item_measurement_is_exits(id):
    measurement = Measurement.objects.filter(item_id=id).exists()
    if measurement:
        return 1
    else:
        return 0