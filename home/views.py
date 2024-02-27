import json
from django.shortcuts import render, redirect
from commons.services import STICHING_SERVICES, get_service_class
from dashboard.services.models import StichingItemRelation, Cart, ItemsInCart
from commons.services import get_preference_class

from dashboard.master.models import UserDetail, User, AddressBook
from home.models import PartnerForm
from django.contrib.auth import logout
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.messages.api import get_messages
from django.contrib.auth.hashers import make_password
import threading

from commons.mail.email_config import contactmessage
# Create your views here.

from commons.user_role import customer_only

@customer_only
def home(request):
    return render(request, "index.html")

@customer_only
def our_services(request):
    all_services = {}
    for service_name, service_obj in STICHING_SERVICES.items():
        all_services[service_name] = list( service_obj.objects.all().values('id', 'name'))
    
    first_page_items = StichingItemRelation.objects.filter(
        category_id = 1,
        service_id = 1, 
        pattern_id = 1,
        finishing_id = 1
    ).all()
    
    if len(all_services) > 0:
        all_services['finishing'][0], all_services['finishing'][1] = all_services['finishing'][1], all_services['finishing'][0]
        
    item_counts = first_page_items.count()
    return render(request, "services/services.html", {'services' : all_services, 'related_items' : first_page_items, 'item_counts' : item_counts})

@customer_only
def our_story(request):
    return render(request, "our-story.html")

@customer_only
def our_work(request):
    return render(request, "our-work.html")

@customer_only
def policy_cancelation_refund(request):
    return render(request, "cancelation_refund_policy.html")

@customer_only
def terms_and_conditions(request):
    return render(request, "terms_and_conditions.html")

@customer_only
def my_profile(request):  
    
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_details = {}
        user_detail = {}   
        family_members = UserDetail.objects.filter(created_by_id=user.id).all()
        storage = get_messages(request)
        info_message = ''
        for message in storage:
            info_message = message
        if info_message:
            storage.used = True
        
        if request.method == "POST":
            try:                    
                user.first_name = request.POST.get('firstName', '').strip()
                user.last_name = request.POST.get('lastName', '').strip()
                user.email = request.POST.get('email', '').strip()
                user.mobile_no = request.POST.get('mobile_no', '').strip() 
                if not user.is_details_added:                    
                    add_new_detail = UserDetail()
                    add_new_detail.user_id = request.user.id
                    add_new_detail.address = request.POST.get('address', '')
                    add_new_detail.pincode = request.POST.get('pincode', '')
                    add_new_detail.location = request.POST.get('city', '')
                    add_new_detail.gender = request.POST.get('gender', '')
                    #add_new_detail.dob = request.POST.get('dob', '')
                    add_new_detail.address_type = request.POST.get('addressType', '')
                    if request.FILES.get('imageUpload'):
                        add_new_detail.image = request.FILES.get('imageUpload', '')
                    
                    add_new_detail.save()
                else:
                    add_new_detail = UserDetail.objects.filter(user_id=request.user.id).last()
                    add_new_detail.user_id = request.user.id
                    add_new_detail.address = request.POST.get('address', '').strip()
                    add_new_detail.pincode = request.POST.get('pincode', '').strip()
                    add_new_detail.location = request.POST.get('city', '').strip()
                    add_new_detail.gender = request.POST.get('gender', '').strip()
                    #add_new_detail.dob = request.POST.get('dob', '')
                    if request.FILES.get('imageUpload'):
                        add_new_detail.image = request.FILES.get('imageUpload', '')
                    add_new_detail.save()
                   
                user.is_details_added = True
                user.save()                    
            except IntegrityError as e:
                return render(request, "my-profile.html", {"user_details" : user_details, 'user_detail' : user_detail ,'user' : user, 'family_members': family_members,'message' : 'email id exists'})                            
            except Exception as e:
                return render(request, "my-profile.html", {"user_details" : user_details, 'user_detail' : user_detail ,'user' : user, 'family_members': family_members, 'message' : 'Something went wrond please try again later.'})                            
            
                
            return redirect(my_profile)
        
        
        
       
        if user.is_details_added:
            user_detail=  UserDetail.objects.filter(user_id=user.id).last()
            user_details = UserDetail.objects.filter(user_id=user.id).all()
            
        return render(request, "my-profile.html", {"user_details" : user_details, 'user_detail' : user_detail ,'user' : user, 'family_members': family_members, 'message' : info_message.message if info_message else '' })
    else:
        return redirect(home)
    

@customer_only
def add_family_members(request):
    user_id = request.user.id     
    if request.method == 'POST':
        mobile_no = request.POST.get('mobile','').strip()
        email = request.POST.get('email','').strip()
        checkemail = User.objects.filter(email=email).exists()
        checkmobile = User.objects.filter(mobile_no=mobile_no).exists()
        if checkemail or checkmobile:
            messages.info(request,'Account alreardy exists with this mobile number/email id')
            return redirect(my_profile)
        else:
            user = User()
            user.first_name = request.POST.get('firstName','').strip()
            user.last_name = request.POST.get('lastName','').strip()
            user.email = email
            user.mobile_no = mobile_no
            user.role = 3
            user.save()

            add_new_detail = UserDetail()
            add_new_detail.user_id = user.id
            add_new_detail.gender = request.POST.get('gender', '')
            if request.POST.get('dob', ''):
                add_new_detail.dob = request.POST.get('dob', '')
            add_new_detail.created_by_id = user_id
            if request.FILES.get('itemImage', ''):
                add_new_detail.image = request.FILES.get('itemImage', '')
            add_new_detail.save()
        
        return redirect(my_profile)



@customer_only
def edit_family_members(request, id):    
    if request.method == 'POST':
        user = User.objects.get(id=id)
        user.first_name = request.POST.get('firstName','').strip()
        user.last_name = request.POST.get('lastName','').strip()
        user.email = request.POST.get('email','').strip()
        user.mobile_no = request.POST.get('mobile','').strip()
        user.role = 3
        user.save()

        add_new_detail = UserDetail.objects.get(user_id=id)
        add_new_detail.gender = request.POST.get('gender', '')
        if request.POST.get('dob', ''):
            add_new_detail.dob = request.POST.get('dob', '')
        if request.FILES.get('itemImage', ''):
            add_new_detail.image = request.FILES.get('itemImage', '')
        add_new_detail.save()
        
        return redirect(my_profile)
    

@customer_only
def add_address_book(request):    
    if request.method == 'POST':
        new_address = AddressBook()
        new_address.user_id = request.user.id
        new_address.first_name = request.POST.get('firstName','').strip()
        new_address.last_name = request.POST.get('lastName','').strip()
        new_address.email = request.POST.get('email','').strip()
        new_address.mobile_no = request.POST.get('mobile','').strip()
        new_address.address = request.POST.get('address','').strip()
        new_address.land_mark = request.POST.get('landmark','').strip()
        new_address.address_type = request.POST.get('addressType')
        new_address.city = request.POST.get('city','').strip()
        new_address.pincode = request.POST.get('pincode','').strip()
        new_address.save()
        return redirect(my_profile)
    

def edit_address_book(request, id):
    if request.method == 'POST':
        new_address = AddressBook.objects.get(id=id)
        new_address.user_id = request.user.id
        new_address.first_name = request.POST.get('firstName','').strip()
        new_address.last_name = request.POST.get('lastName','').strip()
        new_address.email = request.POST.get('email','').strip()
        new_address.mobile_no = request.POST.get('mobile','').strip()
        new_address.address = request.POST.get('address','').strip()
        new_address.land_mark = request.POST.get('landmark','').strip()
        new_address.address_type = request.POST.get('addressType')
        new_address.city = request.POST.get('city','').strip()
        new_address.pincode = request.POST.get('pincode','').strip()
        new_address.save()
        return redirect(my_profile)


@customer_only
def custom_stitching(request):
    return render(request, "custom-stitching.html")

@customer_only
def faqs(request):
    return render(request, "faqs.html")

@customer_only
def book_now(request):
    return render(request, "book-now.html")

@customer_only
def contact(request):
    if request.method == 'POST':
        name= request.POST.get('name','')
        mobile= request.POST.get('mobile','')
        message= request.POST.get('message','')
        tread = threading.Thread(target=contactmessage, args=[name,mobile,message])
        tread.start()
        return render(request, "contact.html",{'message':message})
    
        

    return render(request, "contact.html")

@customer_only
def thank_you(request):
    return render(request, "thankyou.html")

# def my_booking(request):
#     return render(request, "my-booking.html")
@customer_only
def my_booking_items(request):
    return render(request, "my-booking-items.html")

@customer_only
def blogs(request):
    return render(request, "blogs.html")

@customer_only
def fabric_care(request):
    return render(request, "fabric-care.html")

def partner_profile(request):
    if request.method == 'POST':
        
        password = request.POST.get('password','').strip()
        mobile_no = request.POST.get('mobileNumber','').strip()
        email = request.POST.get('email','').strip()
        checkemail = User.objects.filter(email=email).exists()
        checkmobile = User.objects.filter(mobile_no=mobile_no).exists()
        if checkemail or checkmobile:
            messages.info(request,'Account alreardy exists with this mobile number/email id')
            return render(request,'partner-profile.html',{'services':STICHING_SERVICES}) 
        else:
            user = User()
            user.first_name = request.POST.get('firstName','').strip()
            user.last_name = request.POST.get('lastName','').strip()
            user.email = email
            user.mobile_no = mobile_no
            user.password = make_password(password)
            user.role = 4
            user.is_password_set = 1
            user.save()

            add_new_detail = UserDetail()
            add_new_detail.user_id = user.id
            add_new_detail.address = request.POST.get('address', '')
            add_new_detail.pincode = request.POST.get('pincode', '')
            add_new_detail.location = request.POST.get('city', '')
            add_new_detail.gender = request.POST.get('gender', '')
            add_new_detail.address_type = request.POST.get('addressType', '')
            add_new_detail.save()
            
            partner = PartnerForm()
            partner.user_id = user.id
            partner.service_type = request.POST.get('servicesTypePartnerForm','').strip()
            partner.service_name = request.POST.get('servicesPartnerForm','').strip()
            partner.organization_name = request.POST.get('organization','').strip()       
            partner.save() 
            return redirect('partner/') 

    return render(request,'partner-profile.html',{'services':STICHING_SERVICES})