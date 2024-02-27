let createTransactionURL = "/bookings/transaction-order/";

function openJsCheckoutPopupPayTM(orderId, txnToken, amount, payingFor, mainOrderId) {
	var config = {
		"root": "",
		"flow": "DEFAULT",
		// "payMode" : {
		// 	"orders" : ['UPI','CARD']
		// },
		"data": {
			"orderId": orderId,
			"token": txnToken,
			"tokenType": "TXN_TOKEN",
			"amount": amount
		},
		"merchant": {
			"redirect": false
		},
		"handler": {
			"notifyMerchant": function (eventName, data) {
				console.log("notifyMerchant handler function called");
				console.log("eventName => ", eventName);
				console.log("data => ", data);
			},
            "transactionStatus": function (data) {
               
				
				var csrftoken = getCookie('csrftoken');
				$.post(payTMCallbackURL, { 'csrfmiddlewaretoken': csrftoken, 'data': JSON.stringify(data), 'payingFor': payingFor, 'mainOrderId' : mainOrderId }, function (data) {
					window.Paytm.CheckoutJS.close();
					window.location.replace(bookinPageURL);
					//displayOrderStatus(data);
				});   
            }
		}
	};
	if (window.Paytm && window.Paytm.CheckoutJS) {
		// initialze configuration using init method 
		window.Paytm.CheckoutJS.init(config).then(function onSuccess() {
			// after successfully updating configuration, invoke checkoutjs
			window.Paytm.CheckoutJS.invoke();
		}).catch(function onError(error) {
			console.log("error => ", error);
			alert("Session expired please try again after sometime.")
		});
	}
}

function makeTransactionAgainstOrder(orderId, amount, paymentType){
    var csrftoken = getCookie('csrftoken');
    $.post(createTransactionURL,
        { 'csrfmiddlewaretoken': csrftoken, 'orderId': orderId, 'amount': amount, 'paymentType' : paymentType},
        function (data) {           
            if(data.token != ''){
				console.log(data.token);
				console.log(data.orderId);
                openJsCheckoutPopupPayTM(data.orderId, data.token, data.amount, paymentType, data.mainOrderId);                
            }
            else{
				alert("Session expired please try again after sometime.")
                console.log("no token was provided from server side...");
            }
            
        }
    );
}