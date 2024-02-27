let cartUpdateUri = '/bookings/update-cart/'

function deleteCookie(name) {
  document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function setCookie(cName, cValue, expDays) {
  if (expDays) {
    var date = new Date();
    date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
    var expires = "; expires=" + date.toLocaleString();
  }
  else var expires = "";
  document.cookie = cName + "=" + cValue + "; " + expires + "; path=/";
}

function addItemsToCache(itemId, totalItems, estimatedTotal, count, sub_total = 0.0, ttl = 500000) {
  const now = new Date()

  var cachedItems = JSON.parse(localStorage.getItem('cart'));
  var advancePayable = $('#advance-payable').text();
  if (cachedItems && cachedItems.hasOwnProperty("items")) {
    if (count == 0) {
      delete cachedItems['items'][itemId];
      cachedItems['estimatedTotal'] = estimatedTotal;
      cachedItems['totalItems'] = totalItems;
      cachedItems['advancePayable'] = advancePayable;
      // cachedItems['designersPreference'] = "";
      // cachedItems['serviceMode'] = "";
      localStorage.setItem('cart', JSON.stringify(cachedItems));
      // document.cookie="itemsInCart=" + localStorage.getItem("cart") ;

      setCookie("itemsInCart", localStorage.getItem("cart"), 1);
      if (totalItems == 0 && window.location.href == '/services') {
        localStorage.removeItem("cart");
        setCookie("itemsInCart", "");
      }

      return
    }


    cachedItems['items'][itemId] = { 'qty': count, 'sub_total': sub_total };
    cachedItems['estimatedTotal'] = estimatedTotal;
    cachedItems['totalItems'] = totalItems;
    cachedItems['advancePayable'] = advancePayable;
    localStorage.setItem('cart', JSON.stringify(cachedItems));
    //  document.cookie="itemsInCart=" + localStorage.getItem("cart") ;
    setCookie("itemsInCart", localStorage.getItem("cart"), 1);
  }
  else {
    var item = { expiry: now.getTime() + ttl };
    item['items'] = {}
    item['items'][itemId] = { 'qty': count, 'sub_total': sub_total }
    item['estimatedTotal'] = estimatedTotal;
    item['totalItems'] = totalItems;
    item['advancePayable'] = advancePayable;
    // cachedItems['designersPreference'] = "";
    // cachedItems['serviceMode'] = "";
    localStorage.setItem('cart', JSON.stringify(item));
    //document.cookie="itemsInCart=" + localStorage.getItem("cart") ;
    setCookie("itemsInCart", localStorage.getItem("cart"), 1);
  }
}

function updateItemsFromCart(cartId, itemId, selectedItme) {
  let csrftoken = getCookie('csrftoken');
  $.post(cartUpdateUri, { 'csrfmiddlewaretoken': csrftoken, 'cartId': cartId, 'itemId': itemId }, function (resp) {
    if (resp.status == 'ok') {
      selectedItme.closest('.error-msg').hide();
    }
    else {
      selectedItme.closest('.error-msg').show();
    }

  });
}


function handleFilterTab(filterLabel, btnDataControl) {
  $('.row-data').removeClass('active')
  $('.row-data').each(function () {
    var filterTagArr = $(this).attr('data-tag').split(',');
    var categoryFilterLabel = $('#categoryTab .filter-btn.active').attr('data-controls') === undefined ? true : filterTagArr.includes($('#categoryTab .filter-btn.active').attr('data-controls'));
    var serviceFilterLabel = $('#serviceTab .filter-btn.active').attr('data-controls') === undefined ? true : filterTagArr.includes($('#serviceTab .filter-btn.active').attr('data-controls'));
    var finishFilerLabel = $('#finishTab .filter-btn.active').attr('data-controls') === undefined ? true : filterTagArr.includes($('#finishTab .filter-btn.active').attr('data-controls'));
    var patternFilterLabel = $('#patternTab .filter-btn.active').attr('data-controls') === undefined ? true : filterTagArr.includes($('#patternTab .filter-btn.active').attr('data-controls'));
    if (categoryFilterLabel && serviceFilterLabel && finishFilerLabel && patternFilterLabel) {
      $(this).addClass('active')
    }
  })
}

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


$(document).ready(function () {

  $(document).on('click', ".btn.add", function () {
    $(this).next('.quantity-wrapper').toggleClass('active');
    if ($('.quantity-wrapper').hasClass('active')) {
      var totalItems = parseInt($('#total-item').text()) + 1;
      $('#total-item').text(totalItems);
      var itemValue = parseInt($(this).closest('.row-data').find('.priceValue').text());
      var estimatedTotal = parseInt($(this).closest('.row-data').find('.priceValue').text()) + parseInt($("#estimated-total-item").text());
      $("#estimated-total-item").text(estimatedTotal);
      $("#estimatedAmtPaytm").val(estimatedTotal);
      $('.sticky-cart-footer').addClass('show');
      var itemId = $(this).closest('.row-data').find('.priceValue').attr('id');
      var count = $(this).closest('.row-data').find('.quantity-txt').text();
      addItemsToCache(itemId, totalItems, estimatedTotal, count, sub_total = itemValue * parseInt(count));
      if (window.location.pathname == '/bookings/cart/') {
        updateItemsFromCart(cartId, itemId, $(this));
        $('#total-item').text(totalItems);
      }
    }
  })

  $(document).on('click', ".quantity-btn", function () {
    let cartId = $('input[name="cartId"]').val();
    var count = $(this).closest('.quantity-wrapper').find('.quantity-txt').attr('data-count')
    var itemId = $(this).closest('.row-data').find('.priceValue').attr('id');
    if ($(this).hasClass('increase')) {
      var totalItems = parseInt($('#total-item').text()) + 1;
      $('#total-item').text(totalItems);
      var itemValue = parseInt($(this).closest('.row-data').find('.priceValue').text());
      var estimatedTotal = parseInt($(this).closest('.row-data').find('.priceValue').text()) + parseInt($("#estimated-total-item").text());
      $("#estimated-total-item").text(estimatedTotal);
      $("#estimatedAmtPaytm").val(estimatedTotal);
      var count = parseInt(count) + 1;
      $(this).closest('.quantity-wrapper').find('.quantity-txt').attr('data-count', count);
      $(this).closest('.quantity-wrapper').find('.quantity-txt').text(count);

      addItemsToCache(itemId, totalItems, estimatedTotal, count, sub_total = itemValue * parseInt(count));
      if (window.location.pathname == '/bookings/cart/') {
        updateItemsFromCart(cartId, itemId, $(this));
        $('#total-item').text(totalItems);
      }
    }
    else if (count !== "1") {
      var totalItems = $('#total-item').text() - 1
      $('#total-item').text(parseInt(totalItems))
      var estimatedTotal = parseInt(parseInt($("#estimated-total-item").text()) - $(this).closest('.row-data').find('.priceValue').text())
      $("#estimated-total-item").text(estimatedTotal);
      $("#estimatedAmtPaytm").val(estimatedTotal);
      $(this).closest('.quantity-wrapper').find('.quantity-txt').attr('data-count', parseInt(count) - 1)
      $(this).closest('.quantity-wrapper').find('.quantity-txt').text(parseInt(count) - 1)

      var itemValue = parseInt($(this).closest('.row-data').find('.priceValue').text());

      addItemsToCache(itemId, totalItems, estimatedTotal, parseInt(count) - 1, sub_total = itemValue * (parseInt(count) - 1));

      if (window.location.pathname == '/bookings/cart/') {
        updateItemsFromCart(cartId, itemId, $(this));
        $('#total-item').text(totalItems);
      }
    }
    else {
      var totalItems = $('#total-item').text() - 1
      $('#total-item').text(parseInt(totalItems));
      var estimatedTotal = parseInt(parseInt($("#estimated-total-item").text()) - $(this).closest('.row-data').find('.priceValue').text())
      $("#estimated-total-item, #updateItemsFromCart").text(estimatedTotal);
      $("#estimatedAmtPaytm").val(estimatedTotal);
      if (parseInt($('#total-item').text()) === 0) {
        $('.sticky-cart-footer').removeClass('show');
        $("#estimated-total-item").text(0);
      }
      addItemsToCache(itemId, totalItems, estimatedTotal, parseInt(count) - 1, sub_total = (parseInt(count) - 1) * estimatedTotal);
      $(this).closest('.quantity-wrapper').removeClass('active');

      if (window.location.pathname == '/bookings/cart/') {
        updateItemsFromCart(cartId, itemId, $(this));
        $('#total-item').text(totalItems);
        if (totalItems == 0) {
          // $('.sticky-cart-footer').show();
          $('#advance-payable').text(0);
          $(this).closest(".row-data.active").next().find('.btn.btn7.pay-btn.nextBtn').hide();
          $(this).closest(".row-data.active").next().show();
          $(this).closest(".row-data.active").remove();
          $('.stepwizard-row.setup-panel').hide();
          $('.selection-details').hide();
          $('.address-details').hide();
          $('.sticky-cart-footer').hide();
          localStorage.removeItem("cart");
          setCookie("itemsInCart", "");
          return;
          // $('.sticky-cart-footer').closest('.btn.btn7.pay-btn.nextBtn').hide();
        }
        $(this).closest(".row-data.active").remove();
      }
    }
  })

  $('.paymentPlatformHandle').change(function () {
    $('.payment-box').removeClass('selected')
    $(this).parent().addClass('selected')
    $('#paymentPlatform').val($(this).val())
  })
})


$(document).ready(function () {
  var navListItems = $('div.setup-panel div a'),
    allWells = $('.setup-content'),
    allNextBtn = $('.nextBtn'),
    allPrevBtn = $('.prevBtn');

  allWells.hide();

  navListItems.click(function (e) {
    e.preventDefault();
    var $target = $($(this).attr('href')),
      $item = $(this);

    if (!$item.hasClass('disabled')) {
      navListItems.removeClass('btn-primary').addClass('btn-default');
      $item.addClass('btn-primary');
      allWells.hide();
      $target.show();
      $target.find('input:eq(0)').focus();
    }
  });

  allPrevBtn.click(function () {
    var curStep = $(this).closest(".setup-content"),
      curStepBtn = curStep.attr("id"),
      prevStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().prev().children("a");
    prevStepWizard.removeAttr('disabled').trigger('click');
  });

  allNextBtn.click(function () {
    var curStep = $(this).closest(".setup-content"),
      curStepBtn = curStep.attr("id"),
      nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
      curInputs = curStep.find("select[name='serviceMode'],select[name='designersPreference']"),
      //paymentMode = curStep.find("input[name='paymentPlatform']"),
      isValid = false;

    $(".form-group").removeClass("has-error");
    for (var i = 0; i < curInputs.length; i++) {
      if (!curInputs[i].validity.valid) {
        isValid = false;
        $(curInputs[i]).closest(".form-group").addClass("has-error");
        $(curInputs[i]).siblings('.error-msg').show();
      }
      else {
        $(curInputs[i]).siblings('.error-msg').hide();
        isValid = true;
      }
    }

    if (isValid == true) {
      createPaytmOrder(allNextBtn);
    }


  });

  $('div.setup-panel div a.btn-primary').trigger('click');
});




