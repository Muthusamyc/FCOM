function validate_inputs(mobile_no, note){
    if(!$.isNumeric(mobile_no)){
        alert('please enter valid mobile no.');
        return 
    };
    if(mobile_no.length != 10){
        alert('please enter valid mobile no.');
        return 
    };    
    if(note == ''){
        alert('please enter note.');
        return 
    };
    return true;
}

$(document).ready(function(){
    $('#request_callback').on('click', function(){
        var mobile_no = $('#mobile_no').val();
        var note = $('#note').val();
        let csrftoken = getCookie('csrftoken');
        if(validate_inputs(mobile_no, note)){
            $.ajax({
                url: '/api/v1/user/book-callback/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    mobile_no: mobile_no,
                    note:note},
                // dataType: 'json',
                // contentType: 'application/json',
                success: function(data){
                    if(data.status == 'success'){
                        $('.tooltip-drpdown').removeClass('show');
                        $('#mobile_no').val('');
                        $('#note').val('');      
                        window.location.replace('/thank-you')              
                    }
                    else{
                        alert('Something went wrong. Please try again.');
                    }
                }
            });
        };
    });
});



