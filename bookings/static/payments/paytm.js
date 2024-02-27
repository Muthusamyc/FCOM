let createOrderURL = "/bookings/create-order/";
let payTMCallbackURL = "/bookings/paytm-callback";
let bookinPageURL = "/bookings/my-bookings/";


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function invokePayment(cardElement) {
    cardElement.invoke();
}

function displayOrderStatus(data) {

    $('#orderIdCreated').text(data.orderId);   
    $('#orderDate').text(data.orderDate);
    $('#order-Status').text(data.status);
    $('#estimated-total-order').text(data.estimatedAmount);
    $('#advancedAmount-order').text(data.advanceAmount);
    $('#orderStatus').show();

    var itemImages = $('.selected-image');
    var imageData =  data['items'];
    for(var i = 0; i < imageData.length; i++){
        var itemImage  = '<img src="' + imageData[i] + '" alt="Items">';
        console.log(itemImage);
        $('.selected-image').append(itemImage);
    }

    //- <span class="highlighted-text">Paid</span>
    if(data.paymentType == 'estimated'){
        $('.itemstop-title #estimated-total-order').append('- <span class="highlighted-text">Paid</span>')
    }
    else{
        $('.itemstop-title #advancedAmount-order').append('- <span class="highlighted-text">Paid</span>')
    }
    if(data.status != "Order Booked"){
        localStorage.removeItem("cart");
    } 
}

function clearCacheAfterOrderBookedOrFailed(){          
    localStorage.removeItem("cart");
}

function makePayTMTransaction(orderId, token, amount, payingFor, mainOrderId, cartId) {
    //Check if CheckoutJS is available
   
    var config = {
                "root": "",
                "flow": "DEFAULT",
                "data": {
                    "orderId": orderId,
                    "token": token,
                    "tokenType": "TXN_TOKEN",
                    "amount": amount
                },
                "merchant": {
                    "redirect": false
                },
                "payMode": {
                    "labels": {},
                    "filter": [],
                    "order":  ['UPI','CARD', 'NB']
                },
                "handler": {
                    "notifyMerchant": function (eventName, data) {
                        console.log("notifyMerchant handler function called");
                        console.log("eventName => ", eventName);
                        console.log("data => ", data);
                    },
                    "transactionStatus": function (data) {
                        console.log(data);
                    
                        var csrftoken = getCookie('csrftoken');
                        $.post(payTMCallbackURL, { 'csrfmiddlewaretoken': csrftoken, 'data': JSON.stringify(data), 'payingFor': payingFor, 'mainOrderId' : mainOrderId, 'cartId' : cartId }, function (data) {
                            window.Paytm.CheckoutJS.close();
                            console.log("payment status ", data);
                            clearCacheAfterOrderBookedOrFailed(data);
                            window.location.replace(bookinPageURL);
                            //displayOrderStatus(data);
                        });     

                        
                    }
                }
        }
        if (window.Paytm && window.Paytm.CheckoutJS){
            window.Paytm.CheckoutJS.init(config).then(function onSuccess() {
                // after successfully updating configuration, invoke checkoutjs
                window.Paytm.CheckoutJS.invoke();
            }).catch(function onError(error) {
                console.log("error => ", error);
                alert("Session expired please try again after sometime.")
            });     
        }else {
            console.log("element is already rendered!") };
}

function eraseCookie(name) {   
    document.cookie = name+'=; Max-Age=0; path=/';  
}


function createPaytmOrder(allNextBtn){
    let payingFor = allNextBtn.prevObject[0].activeElement.name;
   // let cachedItems = JSON.parse(localStorage.getItem('cart'));
    let payment_type;
    if (payingFor == 'estimatedAmountBtn') {
        payment_type = "estimated";
        
    }
    else {
        payment_type = "advance";
    }
    let bookingType = $('select[name="designersPreference"]').val();
    let serviceType = $('select[name="serviceMode"]').val();

    let carchedData = JSON.parse(localStorage.getItem("cart"));
    var csrftoken = getCookie('csrftoken');
    let cartId = $("input[name='cartId']").val();
    let amount = allNextBtn.prevObject[0].activeElement.children[0].textContent;
    // if(carchedData && carchedData.hasOwnProperty("token")){
    //     makePayTMTransaction(carchedData['orderId'], carchedData['token'], amount, payment_type, carchedData['mainOrderId'], carchedData['cartId']);     
    //     return;
    // }

    $('#bookingType').val(bookingType);
    $('#serviceType').val(serviceType);
    clearCacheAfterOrderBookedOrFailed();
    //eraseCookie("itemsInCart");
    if (bookingType  && serviceType){
        if (payingFor == 'estimatedAmountBtn') {
            $("#estimatedPaymentForm").submit();
            
        }
        else {
            $("#advancePaymentForm").submit();
        }
    }
  
   


    // $.post('create-order-redirect/',
    //     { 'csrfmiddlewaretoken': csrftoken, 'cartId': cartId, 'amount': amount, 'paymentType' : payment_type, 'bookingType' : bookingType, 'serviceType' : serviceType },
    // function (data) {          
        
       

    //     if(data.token != ''){
    //         console.log(data.token);
    //         // carchedData['token'] = data.token;
    //         // carchedData['orderId'] = data.orderId;
    //         // carchedData['mainOrderId'] = data.mainOrderId;
    //         // carchedData['cartId'] = cartId;
    //         // localStorage.setItem("cart", JSON.stringify(carchedData));            
    //         makePayTMTransaction(data.orderId, data.token, data.amount, payment_type, data.mainOrderId, cartId);                
    //     }
    //     else{
    //         console.log("no token was provided from server side...");
    //     }
        
    // })
}


