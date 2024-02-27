let orderStatuUrl = "/bookings/cancel-order/";
let orderApprovalUrl = '/bookings/approve-estimation/';
let deliveryConfirmationUrl = '/bookings/delivery-confirmed/';
let orderRejectUrl = '/bookings/reject-estimation/';
let removeItemUrl = '/bookings/remove-items/';
let customerReviewUrl = '/bookings/customer-review/';
let reshedule_visting_date = '/bookings/reshedule-visit-date/';

function cancelOrderCustomer(orderId) {   
    var csrftoken = getCookie('csrftoken');
    $.post(orderStatuUrl, { 'csrfmiddlewaretoken': csrftoken, 'orderId': orderId }, function (data) 
    {
        console.log(data);
        window.location.reload();
     });
}

function reviewSections() { 
    var csrftoken = getCookie('csrftoken');
   
    var orderId = document.getElementById("order_id").value;
    
    var review = document.getElementById("customer_review").value;
    var customer_services = document.getElementById("customer_services").value;
    var designer = document.getElementById("designer").value;
    var delivery_services = document.getElementById("delivery_services").value;
    $.post(customerReviewUrl, { 'csrfmiddlewaretoken': csrftoken, 'orderId': orderId,'review': review, 
    'customer_services': customer_services, 'designer':designer, 'delivery_services':delivery_services}, function (data) 
    {
        window.location.reload();
     });
}


function apporveOrderCustomer(orderId){
    var csrftoken = getCookie('csrftoken');
    $.post(orderApprovalUrl, { 'csrfmiddlewaretoken': csrftoken, 'orderId': orderId }, function (data) 
    {
        console.log(data);
        window.location.reload();
     });
}

function confirmOrderDelivered(orderId){
    var csrftoken = getCookie('csrftoken');
    $.post(deliveryConfirmationUrl, { 'csrfmiddlewaretoken': csrftoken, 'orderId': orderId }, function (data) 
    {
        console.log(data);
        window.location.reload();
     });
}


function rejectOrderCustomer(orderId){
    var csrftoken = getCookie('csrftoken');
    $.post(orderRejectUrl, { 'csrfmiddlewaretoken': csrftoken, 'orderId': orderId }, function (data) 
    {
        console.log(data);
        window.location.reload();
     });
}

function removeOrderItem(orderId){
    var csrftoken = getCookie('csrftoken');
    $.post(removeItemUrl, { 'csrfmiddlewaretoken': csrftoken, 'orderId': orderId }, function (data) 
    {
        if(data.status == 'item_removed'){
            console.log(data);
            window.location.reload();
            

        }
        else{
            console.log(data);
            document.location.href="/bookings/my-bookings/";
        }
      
        
        
     });
}






function resheduleVistingDdate(orderId){
    var csrftoken = getCookie('csrftoken');
    
    var fromDate = document.getElementById("fromDate").value;
    $.post(reshedule_visting_date, { 'csrfmiddlewaretoken': csrftoken, 'orderId': orderId, 'fromDate': fromDate}, function (data) 
    {
        alert('Reshedule Date has been updated');
        window.location.reload();
        
        
     });
}