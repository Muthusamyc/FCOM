$("#btnSubmitModal").on('click', function (e) {

    $("#logInSubmit").hide();
    $('#signUpSubmitModal').show();
});


$("#btnLoginModal").on('click', function (e) {
    $('#signUpSubmitModal').hide();
    $("#logInSubmit").show();
});


$("#loginSignup").on('click', function (e) {
    $("#signUpCreatePassword").hide();
});


let signUpOTPUri = "/signup-with-otp"

$("#signUpSubmitModal").submit(function (e) {
    e.preventDefault();
    let signUpOtpMobileNumber = $('#signUpOtpMobileNumber').val();
    var csrftoken = getCookie('csrftoken');

    if (signUpOtpMobileNumber != '') {
        if(signUpOtpMobileNumber.length == 10 &&  $.isNumeric( signUpOtpMobileNumber )){
            $('#signUpRequiredError').css('display', 'none');  
        }

        else if( $.isNumeric( signUpOtpMobileNumber )){
            $('#signUpRequiredError').text(errorMsg['mobile_format']);
            $('#signUpRequiredError').css('display', 'block');       
            return false;
        }

        else if(signUpOtpMobileNumber.includes("@")){
            $('#signUpRequiredError').css('display', 'none');       
        }
       

        else{
            $('#signUpRequiredError').text(errorMsg['email_format']);
            $('#signUpRequiredError').css('display', 'block');       
            return false;
        }




        $.post(signUpOTPUri, { "signUpOtpMobileNumber": signUpOtpMobileNumber, 'csrfmiddlewaretoken': csrftoken }, function (resp) {
            if (resp.status == "invalid") {
                $('#signUpRequiredError').text(errorMsg['invalid']);
                $('#signUpRequiredError').css('display', 'block');
                return false;
            }
            if (resp.status == "success") {
                $("#signUpSubmitModal").hide();
                if (resp.mobileNo.includes('@')) { 
                    $('#displaySingUpNumber').text(resp.mobileNo);
                  }
                else{
                    $('#displaySingUpNumber').text('+91 '+ resp.mobileNo);
                }
                $('#signUpOtpBox').show();
            }
            if (resp.status == "failed") {
                $('#signUpRequiredError').text(errorMsg['failed']);
                $('#signUpRequiredError').css('display', 'block');
                return false;
            }
            if (resp.status == "duplicate") {
                $('#signUpRequiredError').text(errorMsg['duplicate']);
                $('#signUpRequiredError').css('display', 'block');
                return false;
            }
        });
    }
    else {
        $('#signUpRequiredError').text(errorMsg['required']);
        $('#signUpRequiredError').css('display', 'block');
    }
});




/** Signup new user with otp */
let signUpOtpVerificationUri = "/verify-signup-otp"
$('#signUpOtpBox').submit(function (e) {
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    var otp_number = ""
    $('#signUpOtpBox .m-2.text-center.form-control.rounded').each(function (d) {
        otp_number += $(this).val();
    });
    $.post(signUpOtpVerificationUri, { "otp": otp_number, 'csrfmiddlewaretoken': csrftoken }, function (resp) {
        console.log(resp)
        if (resp.status == "success") {
            $('#signUpOtpBox').hide();
            $('.reset-password').show();
        }
        if (resp.status == "duplicate") {
            $('#signUpOtpBox .m-2.text-center.form-control.rounded').each(function (d) {
                $(this).val("");
            });
            $("#signUpOtpBox .error-msg").text(errorMsg['duplicate']);
            $('#signUpOtpBox .error-msg').show();
        }
        else {
            $('#signUpOtpBox .m-2.text-center.form-control.rounded').each(function (d) {
                $(this).val("");
            });

            $("#signUpOtpBox .error-msg").text(errorMsg['failed']);
            $('#signUpOtpBox .error-msg').show();
        }
    });
});

let signUpCreatePassword = '/signup-create-password'
$("#signUpCreatePassword").submit(function (e) {
    let csrftoken = getCookie('csrftoken');
    e.preventDefault();
    var password = $("#signUpNewPassword").val()
    var confirmPassword = $("#signupConfirmPassword").val();
    if(password.length < 8 || confirmPassword.length < 8){
        $("#signUpCreatePassword .error-msg").text(errorMsg['shortPassword']);
        $("#signUpCreatePassword .error-msg").show();
        return false;
    }
    
    if (password != confirmPassword) {
        $("#signUpCreatePassword .error-msg").text(errorMsg['passwordMismatch']);
        $("#signUpCreatePassword .error-msg").show();
        return false;
    } else { $("#signUpCreatePassword .error-msg").hide(); }

    $.post(signUpCreatePassword, {'password' : password, 'csrfmiddlewaretoken' : csrftoken}, function(resp){
        if(resp.status == "success"){
            $("#loginModal").modal("hide");
            $("#sigupModalInfo").val(resp.mobile_no);
            if (resp.mobile_no.includes('@')) { 
                $("#sigupModalEmail").val(resp.mobile_no);
                $('#emailid').hide();
              }
            else{
                $("#sigupModalMobileNo").val(resp.mobile_no);
                $('#mobileno').hide();
            }
            $('#logInSubmit').show();
            $('#signupModal').modal("show");
        }
    });
});


let signUpAddDetailsUri = '/signup-add-details'
$('#signup-form').submit(function (e) {
    e.preventDefault();

    const data = {};
    $('#signup-form input, #signup-form select').each(function (index) {
        const input = $(this);
        data[input.attr('name')] = input.val();
    });
    data['csrfmiddlewaretoken'] = getCookie('csrftoken');

    $.post(signUpAddDetailsUri, data, function(resp){
        if (resp.status == "success"){
            $('p.error-msg').hide();
            $('#thankyou-modal').addClass("show");
            $('#signupModal').trigger("reset");
            $('#signupModal .btn-close').click();
            // window.location.reload();
        }
        else{
            console.log(resp);
        }
    });    
});