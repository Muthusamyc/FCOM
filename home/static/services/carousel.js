// Slider Automatic
var myIndex = 0;
carousel();
function carousel() {
    var i;
    var x = document.getElementsByClassName("carousel-item");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    myIndex++;
    if (myIndex > x.length) { myIndex = 1 }
    x[myIndex - 1].style.display = "";
    setTimeout(carousel, 4000); // Change image every 2 seconds
}
// Slider Dot
var slideIndex = 1;
showDivs(slideIndex);
function plusDivs(n) {
    showDivs(slideIndex += n);
}
function currentDiv(n) {
    showDivs(slideIndex = n);
}
function showDivs(n) {
    var i;
    var x = document.getElementsByClassName("carousel-item");
    var dots = document.getElementsByClassName("dot1");
    if (n > x.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = x.length }
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" w3-white", "");
    }
    x[slideIndex - 1].style.display = "";
    //dots[slideIndex-1].className += " w3-white";
}