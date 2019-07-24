$(function () {
    $('#datepicker0').datepicker();
});

$('.glyphicon-calendar').click(function() {
   $("#datepicker0").focus();
 });

var date = new Date();
date.setDate(date.getDate()+1);
$("#datepicker0").datepicker({
 minDate: date
});
$("#datepicker0").datepicker("setDate", "date");

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
