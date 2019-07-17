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
   var department = object.value;
   var url = "/laborstatusform/getPositions/" + department;
       $.ajax({
         url: url,
         dataType: "json",
         success: function (response){
            fill_positions(response)
         }
       })
 }

function fill_jobtype(response){
  var selected_jobtype = document.getElementById("jobtype");
  $("#jobtype").empty();
  for (var key in response){
    var options = document.createElement("option")
    options.text = response[key]["job type"].toString();
    options.value = key;
    console.log(options.value, "heeyy")
    selected_jobtype.appendChild(options);
  }
  $(".selectpicker").selectpicker('refresh');
}

 function getTerm(obj){
   var term = obj.value;
   var url  = "/laborstatusform/getjobtype/" + term;
   $.ajax({
     url: url,
     dataType: "json",
     success: function(response){
       fill_jobtype(response)
     }
   })
 }

function fill_hoursperweek(response){
  var selected_hours_perweek = document.getElementById("hours_perweek");
  $("#hours_perweek").empty();
  for (var key in response){
    var options = document.createElement("option");
    options.text = response[key]["Weekly Hours"].toString();
    options.value = key;
    selected_hours_perweek.appendChild(options);
  }
  $('.selectpicker').selectpicker('refresh');
}

function getjobtype(obj){
  var jobtype = obj.value;
  var url = "/laborstatusform/gethoursperweek/" + jobtype;
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      fill_hoursperweek(response)
    }
  })
}
