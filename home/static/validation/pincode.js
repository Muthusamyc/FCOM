$('#pincode').on('keypress', function (e) {
    var $this = $(this);
    var regex = new RegExp('^[0-9\b]+$');
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    // for 10 digit number only
    if ($this.val().length > 5) {
        e.preventDefault();
        return false;
    }
    // if (e.charCode < 54 && e.charCode > 47) {
    //     if ($this.val().length === 0) {
    //         e.preventDefault();
    //         return false;
    //     } else {
    //         return true;
    //     }
    // }
    if (regex.test(str)) {
        return true;
    }
    e.preventDefault();
    return false;
});