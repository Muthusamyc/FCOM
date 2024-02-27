from django.shortcuts import redirect, render
from dashboard.services.models import Order, PayTMTransactionDetails

def paytm_refund(request):
    if request.method == "POST":
        order_id = request.POST.get('orderId', '')
        refund_amt = request.POST.get('refundAmt', '')
        zorder = PayTMTransactionDetails.objects.get(order_id=order_id)
        
        
    
    