// $('#logInSubmit').submit(function (e){
//     e.preventDefault();

//     const data = {};
//     data['userId'] = $('#userId').val();
//     data['password'] = $('#password').val();       
    

//     $.ajax({
//             type: "POST",
//             url: "/api/v1/user/signin/",
//             data: JSON.stringify(data),
//             contentType: "application/json",
//             dataType: "json",
//             header: {
//                 'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
//             },
//             success: function (result) {
//                 if (result.message == "loggedin") {
//                     if(location.pathname == '/services'){
//                         window.location.replace('/bookings/cart');
//                     }
//                     else{
//                         window.location.reload();
//                     }
                   
//                 }   
//                 else if (result.message == "loggingFailed"){
//                     $('#logging-alert-id').css('display', 'block');
//                     $('#logging-alert-id').addClass('show');
//                 }                 
//                 else {
                    
//                 }
//             },
//             error: function (error) {
//                 alert(error);
//             }
//         });
// });

// $(document).ready(function () {
//     $('.category-box').on('click', function () {
//         $('.category-box').not(this).removeClass('selected');
//         $(this).toggleClass("selected");
//         const user_type = $(this).children()[1].textContent;

//         let userType = 3;
//         if (user_type == 'Customer') {
//             userType = 3;
//         }
//         else {
//             userType = 2
//         }

//         $('#user_type').val(userType);
//     });
//     $("#success-modal .btn-close,#thankyou-modal .btn-close").click(function(){
//         $(this).closest(".modal").removeClass('show')
//     })
//     $('#signup-form').submit(function (e) {
//         e.preventDefault();

//         var password = $("#signUpPassword").val()
//         var confirmPassword = $("#confirmPassword").val();
//         if(password != confirmPassword){
//             $('#password-alert').addClass('show');
//             return false;
//         }else { $('#password-alert').addClass('hide'); }

//         const data = {};
//         $('#signup-form input, #signup-form select').each(function (index) {
//             const input = $(this);
//             data[input.attr('name')] = input.val();
//         });

//         $.ajax({
//             type: "POST",
//             url: "/api/v1/user/signup/",
//             data: JSON.stringify(data),
//             contentType: "application/json",
//             dataType: "json",
//             header: {
//                 'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
//             },
//             success: function (result) {
//                 if (result.message == "ok") {
//                     $('p.error-msg').hide();
//                     $('#success-modal').addClass("show");
//                     $('#signupModal').trigger("reset");
//                     $('#signupModal .btn-close').click();
//                 }
//                 else {
//                     $('p.error-msg').show();
                    
//                 }
//             },
//             error: function (error) {
//                 alert(error);
//             }
//         });
//     });
// });

let SEND_OTP_URI = "/send-opt"

let errorMsg = {
    'required' : "Please enter your mobile number",
    'mobile_format' : "Please enter 10 digits mobile number.",
    'email_format' : "Please enter vaild email id.",
    'invalid' : "Mobile number not registered.",
    'failed' : "Something went wrong, please try again later.",
    'duplicate' : "Account alreardy exists with this mobile number/email id.",
    'passwordMismatch' : "Password doesn't match",
    'shortPassword' : "Password should be atleast 8 Characters.",
    'newuser' : "User not registered.",
}

$('#logInSubmit').submit(function (e){
    // $("#logInSubmit").hide();
    // $('#otpBox').show();
    e.preventDefault();
    let userId = $("#otp_mobile_no").val();
    var csrftoken = getCookie('csrftoken');
    if(userId != ''){
        if(userId.length == 10 &&  $.isNumeric( userId )){
            $('#userIdRequiredError').css('display', 'none');  
        }

        else if( $.isNumeric( userId )){
            $('#userIdRequiredError').text(errorMsg['mobile_format']);
            $('#userIdRequiredError').css('display', 'block');       
            return false;
        }

        else if(userId.includes("@")){
            $('#userIdRequiredError').css('display', 'none');       
        }
       

        else{
            $('#userIdRequiredError').text(errorMsg['email_format']);
            $('#userIdRequiredError').css('display', 'block');       
            return false;
        }
       
        $.post(SEND_OTP_URI, {"userId" : userId, 'csrfmiddlewaretoken': csrftoken}, function(resp){
            if(resp.status=="invalid"){
                $('#userIdRequiredError').text(errorMsg['invalid']);
                $('#userIdRequiredError').css('display', 'block');       
                return false;
            }
            if(resp.status=="ok"){
                $("#logInSubmit").hide();
                if (resp.mobileNo.includes('@')) { 
                    $('#displayUserNumber').text(resp.mobileNo);
                  }
                else{
                    $('#displayUserNumber').text('+91 '+ resp.mobileNo);
                }
                $('#otpBox').show();
            }
            if(resp.status=="failed"){
                $('#userIdRequiredError').text(errorMsg['failed']);
                $('#userIdRequiredError').css('display', 'block');       
                return false;
            }
            if(resp.status == "newuser"){
                $('#userIdRequiredError').text(errorMsg['newuser']);
                $('#userIdRequiredError').css('display', 'block');       
                return false;
            }
        });
    }
    else{
        $('#userIdRequiredError').text(errorMsg['required']);
        $('#userIdRequiredError').css('display', 'block');       
    }
});

let VERIFY_OTP_URI = "/verfify-otp"
$('button[name="otpLoginBtn"]').on('click', function(){
    var otp_number = ""
    $('#otpBox .m-2.text-center.form-control.rounded').each(function(d){
        otp_number += $(this).val();
    });
    console.log(otp_number);
    var csrftoken = getCookie('csrftoken');
    $.post(VERIFY_OTP_URI, { "otp" : otp_number,  'csrfmiddlewaretoken': csrftoken}, function(resp){
        
      if(resp.status=="success"){
        if(window.location.pathname == '/services'){
            window.location.href = cartPageUrl;
        }
        else{
            window.location.reload();
        }        
      }
    });
});
