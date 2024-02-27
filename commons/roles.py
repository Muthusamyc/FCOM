ADMIN = 1
DESIGNER = 2
CUSTOMER = 3
PARTNER = 4

ROLE_CHOICES = (
    (ADMIN, 'Admin'),
    (DESIGNER, 'Designer'),
    (CUSTOMER, 'Customer'),
    (PARTNER, 'Partners'),
)

ROLE_CHOICES_MAP = {
    'admin' : ADMIN,
    'customer' : CUSTOMER,
    'designer' : DESIGNER,
    'partner' : PARTNER
}

def is_user_superadmin(request):    
    return request.is_superuser

from django import template

register = template.Library()

@register.simple_tag
def get_role_name(request):
    return ROLE_CHOICES[request.user.role]


