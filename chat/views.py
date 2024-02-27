from email import message
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.contrib.auth import get_user_model
from .models import Messages

from commons.roles import DESIGNER
from dashboard.master.models import User, UserDetail
from dashboard.services.models import DesingerAssignedOrders


def private_chat_home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    
    if request.user.is_superuser:
        users = User.objects.exclude(id=request.user.id)
    if request.user.role == DESIGNER:
        order_list = DesingerAssignedOrders.objects.filter(
            designer_id=request.user.id
        ).distinct()
        users = User.objects.filter(
            id__in=[item.order.made_by.id for item in order_list]
        )
        
        page_no = request.GET.get('page', 1)
        page_no, limit = page_no, 10
        paginator = Paginator(users, limit)
        
        
        try:
            users = paginator.page(page_no)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users =  []
        
    
    return render(request, "chat.html", context={"users": users})


def chatPage(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    user_obj = User.objects.get(id=id)

    if request.user.is_superuser:
        users = User.objects.exclude(id=request.user.id)
    if request.user.role == DESIGNER:
        # TODO: improve sql query to relate designer with customer
        order_list = DesingerAssignedOrders.objects.filter(
            designer_id=request.user.id
        ).distinct()
        users = User.objects.filter(id__in=[order.user_id for order in order_list])

    if request.user.is_authenticated:
        if request.user.id > user_obj.id:
            thread_name = f"chat_{request.user.id}-{user_obj.id}"
        else:
            thread_name = f"chat_{user_obj.id}-{request.user.id}"
        message_objs = Messages.objects.filter(thread_name=thread_name).all()
        senders = {}
        send_messg = []
        username = user_obj.first_name + " " + user_obj.last_name
        for i, mesg in enumerate(message_objs):
            user_obj_temp = User.objects.get(id=mesg.sender)
            senders[user_obj_temp.id] = f"{user_obj_temp.username}"
            send_messg.append([f"{mesg.sender}", f"{mesg.message}", mesg.timestamp])
        return render(
            request,
            "messages.html",
            context={
                "user": f"{user_obj.id}",
                "users": users,
                "messages": message_objs,
                "username": username,
                "count": len(send_messg),
            },
        )
