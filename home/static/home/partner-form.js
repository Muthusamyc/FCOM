$('#partner_menu').on('click', function () {
    var csrftoken = getCookie('csrftoken');

    var partnerFormService = JSON.parse(localStorage.getItem("partnerFormServices"));

    if (partnerFormService == null) {
        $.ajax({
            url: "/partner-services",
            method: "GET",
            headers: { 'X-CSRFToken': csrftoken },

        }).done(function (response) {
            var serviceTypeSelect = $('#servicesTypePartnerForm');
            $.each(response.all_services, function (data) {
                serviceTypeSelect.append($('<option></option>').val(data).html(data));                

            });
            localStorage.setItem("partnerFormServices", JSON.stringify(response));
            console.log(response.all_services);
            
        }).fail(function (error) {
            console.log(error);
        });
    }
    else{
        
        var serviceTypeSelect = $('#servicesTypePartnerForm');
        $.each(partnerFormService.all_services, function (data) {
            serviceTypeSelect.append($('<option></option>').val(data).html(data));
        });
       
    };

    $("#servicesTypePartnerForm").on("change", function(){ 
        $('#servicesPartnerForm').prop('disabled', false);
        var selectedServiceForm =  $(this).val();
        if(partnerFormService == null){
            partnerFormService = JSON.parse(localStorage.getItem("partnerFormServices"));
        }
        var services = partnerFormService.all_services[selectedServiceForm];
        var selectServices = $('#servicesPartnerForm');
        $.each(services, function(data){
            selectServices.append($('<option></option>').val(services[data].name).html(services[data].name));       
        })

    });


    $('#partner-form').on("submit", function() {
        var inputData = {}
        $("form#partner-form :input").each(function(){
            var input = $(this); 
            inputData[input.attr("name")] = input.val();
           });
        
        $.ajax({
            url: "/partner-services",
            method: "POST",
            headers: { 'X-CSRFToken': csrftoken },
            data:inputData

        }).done(function (response) {
            if(response.status == "success"){
                $("#partnerModal").modal("hide");
                $("form#partner-form :input").each(function(){
                    $(this).val('');                
                   });
                window.location.replace('/thank-you')              
            }
            else{
                $("#partnerModal").modal("hide");
                alert("something went wrong");
            }            
            
        }).fail(function (error) {
            alert("something went wrong");
            console.log(error);
        });
    });


})