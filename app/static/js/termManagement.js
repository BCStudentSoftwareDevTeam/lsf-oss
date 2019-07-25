$(function () {
    $('.form-control').datepicker({autoSize: true});
});

$('.glyphicon-calendar').click(function() {
   $(".form-control").focus();
 });

var date = new Date();
date.setDate(date.getDate());
$(".form-control").datepicker({
 minDate: date
});
$(".form-control").datepicker("setDate", "date");

// var acc = document.getElementsByClassName("accordion");
// var i;
//
// for (i = 0; i < acc.length; i++) {
//  acc[i].addEventListener("click", function() {
//    this.classList.toggle("active");
//    var panel = this.nextElementSibling;
//    if (panel.style.display === "block") {
//      panel.style.display = "none";
//    } else {
//      panel.style.display = "block";
//    }
//  });
// }
