$(document).ready(function(){
    $('[data-tooltip="true"]').tooltip();
});


 var j = jQuery.noConflict();
 j( function() {
     j( "#datetimepicker1, #datetimepicker2" ).datepicker();
 } );


function fill_positions(response) {
  var selected_positions = document.getElementById("position");
  $("#position").empty();
  for (var key in response) {
    var options = document.createElement("option");
    options.text = response[key]["position"].toString();
    options.value = key;
    selected_positions.appendChild(options);

  }
  $('.selectpicker').selectpicker('refresh');

}

 function getDepartment(object) {
   var department = object.value
   var url = "/laborstatusform/getPositions/" + department;
       $.ajax({
         url: url,
         dataType: "json",
         success: function (response){
            fill_positions(response)

         }
       })
 }
