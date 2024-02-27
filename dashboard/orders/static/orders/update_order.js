function populateItemsData(selectedServicecs) {
    var csrftoken = getCookie('csrftoken');


    $.ajax({
        type: "POST",
        //  url: "/api/v1/user/get-items/" +  jQuery.param({ page: obj.page}),
        url: "/api/v1/user/get-items-from-desingers/",
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'data': JSON.stringify(selectedServicecs),
            'page': 1,
            'limit': 100
        },
        beforeSend: function (msg) {
            $(".loader").addClass("show");
        },
        success: function (result) {
            if (result.message == "ok") {
                $('#item').empty();
                $('#item').append('<option value="">Select Item </option>');
                if(result.item_counts > 0){
                    let itemsCunter = "Items found " + result.item_counts
                    $('#searchedItemsCount').text(itemsCunter);
                    $('#searchedItemsCount').show();
                }

                for (var i = 0; i < result.first_page_items.length; i++) {                        
                    console.log(result.first_page_items[i]);
                    $(new Option(result.first_page_items[i].item__name, result.first_page_items[i].id)).appendTo('#item');                    
                }

                if(result.item_counts == 0){
                    $("#searchedItemsError").show();
                }
                else{
                    $("#searchedItemsError").hide();
                }
            }
            else {

            }
        },
        error: function (error) {
            console.log(error.responseText);
        }
    });
}

$("#search-order-item").on( 'submit', function (e) {

    var selectedServicecs = {
        'category': "1",
        'service': "1",
        'finishing': "2",
        'pattern': "1",
        'items': []
    }

    var services = {};

    const data = {};
    $('#search-order-item select').each(function (index) {
        const input = $(this);
        data[input.attr('name')] = input.val();
    });

    populateItemsData(data);
    
});



$("#add-order-item").on( 'submit', function (e) {    
    const data = {};
    $('#add-order-item select').each(function (index) {
        const input = $(this);
        data[input.attr('name')] = input.val();
    });

    populateItemsData(data);
    
});


//////////////////////////////// Update Individual Item Price By Designer /////////////////////////////
// let designerUpdateItemPrice = "/order/update-item-price/"
// $('#updateItemPrice').submit(function() {
//     let newItemPriceForOrder = $('#itemUpdatedPrice').val();
//     let csrftoken = getCookie('csrftoken');

//     $.post(designerUpdateItemPrice, {
//         'csrfmiddlewaretoken': csrftoken,
//         'newItemPriceForOrder' : newItemPriceForOrder
//     }, function(resp){
//         if(resp.status == "success") {
//             window.location.reload();
//         }
//     });
// });

// $('#editItem').on('click', function(){
//     let editItem = $(this).val();
//     $('#itemId').val(editItem);
// })