$('.form-control').datepicker()
   .on('change', function(e) {
     console.log($(this).data('id'));
     alert($(this).data('id'));
   });

$('.glyphicon-calendar').click(function() {
   $(".form-control").focus();
 });

var date = new Date();
date.setDate(date.getDate());
$(".form-control").datepicker({
});




// $.ajax({
//   type: "POST"
//   url:"/termManagement" +
// })
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
