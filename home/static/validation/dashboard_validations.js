$(function() {
  $("form[name='form_validation']").validate({
    rules: {
      first_name: "required",
      last_name: "required",
      mobile_no: {
        required: true,
        number: true,
        minlength: 10,
        maxlength: 10
          },
      email: {
        required: true,
        email: true
      },
      password: {
        required: true,
        minlength: 7
      }
    },
    messages: {
      first_name: "Please enter your firstname",
      last_name: "Please enter your lastname",
      mobile_no: {
        required: "Please provide a Mobile Number",
        minlength: "Please enter a valid mobile number"
      },
      password: {
        required: "Please provide a password",
        minlength: "Your password must be at least 7 characters long"
      },
      email: "Please enter a valid email address"
    },
    submitHandler: function(form) {
      form.submit();
    }
  });
});
