$('.form-control').datepicker()
   .on('change', function(e) {
     console.log($(this).data('startEnd'));
     alert($(this).data('startEnd'));
   });

$('.glyphicon-calendar').click(function() {
   $(".form-control").focus();
 });

var date = new Date();
date.setDate(date.getDate());
$(".form-control").datepicker({
});

function update_startDate(response){
  console.log(response)
}

function getDate(obj) {
  var termStart = obj.value;
  console.log(obj)
  console.log(termStart)
  console.log("hi")
  var url ="/termMangement/getDate/" + termStart;
    $.ajax({
      url: url,
      datatype: "json",
      success: function(response){
        update_startDate(response)
      }
    })
}


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
