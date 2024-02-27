from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
# Create your models here.
from commons.roles import ROLE_CHOICES

from fcom import settings

   
class User(AbstractUser):
    username = None
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    email = models.EmailField(verbose_name='email', max_length=100, unique=True, null=True)
    mobile_no = models.CharField(max_length=50, null=True, unique=True)
    is_details_added = models.BooleanField(default=False, null=True)
    is_password_set = models.BooleanField(default=False, null=True)
    is_user_online = models.BooleanField(default=False, null=True)
    USERNAME_FIELD = 'email'
   # REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'username', 'mobile_no']
    REQUIRED_FIELDS = ['mobile_no']
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    mobile_no = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=50, null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=200, null=True)
    land_mark = models.CharField(max_length=200, null=True)
    address_type = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=200, null=True)
    latitude = models.CharField(max_length=200, null=True)
    last_logged_in = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='created_by')
    modified_by = models.IntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    is_shipping_address = models.BooleanField(null=True, default=False)
    image = models.ImageField(upload_to= settings.USER_PROFILE_UPLOAD_PATH, null=True)       
    #created_on = models.DateTimeField(auto_now_add=True, null=True)
    #updated_on = models.DateTimeField(auto_now=True, null=True)
    

    class Meta:
        verbose_name = _("user-detail")
        verbose_name_plural = _("user details")
    
    @classmethod
    def create(cls, request):        
        #create user credentials here
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')        
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', '')
        mobile_no = request.POST.get('mobile_no', '').strip()
        new_user = User(
            first_name=first_name,
            last_name = last_name,            
            email = email,
            password = make_password(password),
            mobile_no = mobile_no,
            role= role
        )
        
        new_user.save()

        #create user group here
        mobile_no = request.POST.get('mobile_no', '').strip()
        gender = request.POST.get('gender', '')
        dob = request.POST.get('dob', '')
        address = request.POST.get('address', '')
        land_mark = request.POST.get('landmark', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        country = request.POST.get('country', '')
        pincode = request.POST.get('pincode', '')
        # longitude = request.POST.get('longitude', '')
        # lattitude = request.POST.get('lattitude', '')
        created_on = datetime.now()
        created_by = request.user
        sub_user = cls(
            user_id = new_user.id,
            mobile_no = mobile_no,
            gender = gender,
            dob = dob,
            address = address,
            land_mark = land_mark,
            city = city,
            state = state,
            country = country,
            pincode = pincode,
            # longitude = longitude,
            # latitude = lattitude,            
            created_by=created_by)
        sub_user.save()        
        new_user.is_details_added = True
        new_user.save()

    @classmethod
    def list(cls,request):
        users = cls.objects.filter(user__is_active=1).all()
        return users

    @classmethod
    def edit(cls, request,id):        
        user = UserDetail.objects.get(id=id)
        return user


    @classmethod
    def delete(cls, request, user_id):
        user = User.objects.get(id=id)
        user.delete()
        return user

class PartnerGallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100,null=True)
    image = models.ImageField(
        upload_to=settings.PARTNER_GALLERY_UPLOAD_PATH, null=True)  
    



class AddressBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    mobile_no = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)
    land_mark = models.CharField(max_length=200, null=True)
    address_type = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=50, null=True)
