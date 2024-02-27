from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from payment_gateway.paytm import config, PaytmChecksum


@csrf_exempt
def paytm_callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]                
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = PaytmChecksum.verifySignature(paytm_params, config.PAYTM_MERCHANT_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"    
    print(received_data)
    return render( request,"payment_gateway/paytm.html", { 'data' : received_data })