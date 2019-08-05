var j = jQuery.noConflict();
j( function() {
    j("#datepicker0").datepicker({

    });
} );

$('.glyphicon-calendar').click(function() {
   $("#datepicker0").focus();
 });

var date = new Date();
date.setDate(date.getDate()+1);
$("#datepicker0").datepicker({
  minDate: date
});
$("#datepicker0").datepicker("setDate", "date");

// var newDate
// function getDate(obj){
//   newDate = obj.value
//   console.log(newDate);
// }
//
// var releaseCondition
// function getCondition(obj){
//   releaseCondition = obj.value
//   console.log(releaseCondition);
// }
//
// var releaseReason
// function getReason(obj){
//   releaseReason = obj.value
//   console.log(releaseReason);
// }


$(function() {
   $("#submit").click(function() {
    if($("#condition").val() == "" || $("#datepicker0").val() == "" || $("#reason").val() == "") {
      category = "danger"
      msg = "Please fill out all fields before submitting.";
      $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
      $("#flasher").delay(3000).fadeOut()
    }
    else {
      $("#modal").modal("show");
    }
   });
});


// function createReleaseForm() {
//   console.log("I started here");
//   $.ajax({
//     method: "POST",
//     url: "/index/second",
//     dataType: "json",
//     contentType: "application/json",
//     data: JSON.stringify({"deptName": releaseCondition}),
//     processData: false,
//     success: function(response) {
//   //      console.log(response);
//       if(response["Success"]) {
//         category = "info"
//         var departmentID = $("#dept_btn_" + department);
//         //console.log(departmentID);
//         if ($(departmentID).hasClass("btn-success")){
//
//         }
//         else {
//           console.log("I was not succesful");
//         }
//
//       }
//     }
//   })
// }
