$(document).ready(function(){
    $('[data-tooltip="true"]').tooltip();
});

 var j = jQuery.noConflict();
 j( function() {
     j( "#datetimepicker1, #datetimepicker2" ).datepicker();
 } );

$(document).on('keyup', 'input[name=contracthours]', function () {
   var _this = $(this);
   var min = parseInt(_this.attr('min')) || 1; // if min attribute is not defined, 1 is default
   var val = parseInt(_this.val()) || (min - 1); // if input char is not a number the value will be (min - 1) so first condition will be true
   if(val < min)
       _this.val( min );
});

$("#ContractHours").hide();
$("#Hours_PerWeek").hide();
$("#JopTypes").hide();
$("#Student").hide();
$("#Position").hide();
$("#primary_for_secondary").hide();
$("#plus").hide();
$("#mytable").hide();

function show_access_level(obj){
  $("#ContractHours").hide();
  $("#Hours_PerWeek").hide();
  $("#JopTypes").hide();
  $("#Student").hide();
  $("#Position").hide();
  $("#plus").hide();
  $("#primary_for_secondary").hide();
  var termcode = obj.value
  var whichterm = termcode.toString().substr(-2);
  if (whichterm != 11 && whichterm !=12) { // Summer term or any other break period
    $("#Student").show();
    $("#Position").show();
    $("#ContractHours").show();
    $("#plus").show();
  }
  else{ // normal semester like Fall or Spring
    $("#Student").show();
    $("#Position").show();
    $("#Hours_PerWeek").show();
    $("#JopTypes").show();
    $("#plus").show();
  }
}

function secondary_access(obj){
  var jobtype = obj.value;
  if (jobtype == "Secondary"){
    $("#primary_for_secondary").show();
  }
  else{
    $("#primary_for_secondary").hide();
  }
}


function fill_positions(response) {
  var selected_positions = document.getElementById("position");
  if (selected_positions){
    $("#position").empty();
    for (var key in response) {
      var options = document.createElement("option");
      options.text = response[key]["position"].toString();
      options.value = key;
      selected_positions.appendChild(options);
    }
    $('.selectpicker').selectpicker('refresh');
  }
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

function fill_hoursperweek(){
  var selected_hours_perweek = document.getElementById("hours_perweek");
  var jobtype = $("#jobtype").val();
  if (selected_hours_perweek){
    $("#hours_perweek").empty();
    if (jobtype == "Primary"){
      var options = document.createElement("option");
      var dict = {
        10: "10",
        15: "15",
        20: "20"}
      for (var key in dict){
        selected_hours_perweek.options[selected_hours_perweek.options.length]=
        new Option(dict[key], key);
      }
    }
    else if (jobtype == "Secondary") {
      var options = document.createElement("option");
      var dict = {
        5: "5",
        10: "10"}
      for (var key in dict){
        selected_hours_perweek.options[selected_hours_perweek.options.length]=
        new Option(dict[key], key);
      }
    }
    $('.selectpicker').selectpicker('refresh');
  }
}

function fillprimarysupervisor(response){
  var primary_supervisor = document.getElementById("primary_supervisor")
  if (primary_supervisor){
    $("#primary_supervisor").empty();
    for (var key in response){
      var options = document.createElement("option")
      options.text = response[key]["Primary Supervisor FirstName"].toString() + " " + response[key]["Primary Supervisor LastName"].toString();
      options.value = key;
      primary_supervisor.appendChild(options)
    }
    $('.selectpicker').selectpicker('refresh')
  }
}

function getstudent(obj){
  var student = obj.value;
  var term = $("#term").val();
  var url = "/laborstatusform/getstudents/" + term +"/" +student;
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      fillprimarysupervisor(response)
    }
  })
}
// TABLE
function displayTable() {
  $("#mytable").show();
  $("#job_table").hide();
  $("#hours_table").hide();
  $("#primary_table").hide();
  $("#contract_table").hide();

  var termcode = $('#term').val();
  var whichterm = termcode.toString().substr(-2);

  if (whichterm != 11 && whichterm !=12) {
    checkBreaks();
  }
  else {
    checkDuplicate();
  }

}


function checkDuplicate() {
    var table = document.getElementById("mytable");
    var student = document.getElementById("student");
    var studentname = student.options[student.selectedIndex].text;
    var position = document.getElementById("position");
    var positionname = position.options[position.selectedIndex].text;
    var jobtype = document.getElementById("jobtype");
    var jobtypename = jobtype.options[jobtype.selectedIndex].text;

    for(const tr of table.querySelectorAll("thead tr")) {
       const td0 = tr.querySelector("td:nth-child(1)");
       const td1 = tr.querySelector("td:nth-child(2)");
       const td2 = tr.querySelector("td:nth-child(3)");
       const td3 = tr.querySelector("td:nth-child(4)");
       const td4 = tr.querySelector("td:nth-child(5)");

       if ((td0.innerHTML == studentname) && (jobtypename == "Primary")) {
          category = "danger";
          msg = `Match found for ${studentname} and Primary. Insert rejected`;
          $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>');
          $("#flasher").delay(4000).fadeOut();
          $("#job_table").show();
          $("#hours_table").show();
          $("#primary_table").hide();
          return;
          }
       if ((td0.innerHTML == studentname) && (td2.innerHTML == "Secondary") && (td1.innerHTML == positionname)) {

          category = "danger";
          msg = `Match found for ${studentname} , ${positionname} and Secondary. Insert rejected`;
          $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>');
          $("#flasher").delay(4000).fadeOut();
          $("#job_table").show();
          $("#hours_table").show();
          $("#primary_table").show();
          return;
         }

       if(!td0 || !td1 || !td2 || !td3 || !td4) { //If we are missing cells skip it
       continue }
  }
    CheckAcademicYear();
}


function checkBreaks() {
  $("#mytable").show();
  $("#job_table").hide();
  $("#hours_table").hide();
  $("#primary_table").hide();
  $("#contract_table").show();

  var table = document.getElementById("mytable");
  var student = document.getElementById("student");
  console.log(student)
  var studentname = student.options[student.selectedIndex].text;
  console.log(studentname);
  var position = document.getElementById("position");
  var positionname = position.options[position.selectedIndex].text;
  var contracthoursname = document.getElementById("contracthours").value;
  console.log(contracthoursname);
 // Summer term or any other break period
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = studentname;
  cell2.innerHTML = positionname;
  cell3.innerHTML = contracthoursname;
  $("#contracthours").val('');
  $("#position").val('default');
  $("#position").selectpicker("refresh");
  $("#student").val('default');
  $("#student").selectpicker("refresh");
}

function CheckAcademicYear() {
    $("#mytable").show();
    $("#job_table").show();
    $("#hours_table").show();
    $("#primary_table").hide();
    $("#contract_table").hide();

    var table = document.getElementById("mytable");
    var student = document.getElementById("student");
    var studentname = student.options[student.selectedIndex].text;
    var position = document.getElementById("position");
    var positionname = position.options[position.selectedIndex].text;
    var jobtype = document.getElementById("jobtype");
    var jobtypename = jobtype.options[jobtype.selectedIndex].text;
    var hours_perweek = document.getElementById("hours_perweek");
    var hours_perweekname = hours_perweek.options[hours_perweek.selectedIndex].text;
    var primary_supervisor = document.getElementById("primary_supervisor");
    var primary_supervisorname = primary_supervisor.options[primary_supervisor.selectedIndex].text;

    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);

    cell1.innerHTML = studentname;
    cell2.innerHTML = positionname;
    cell3.innerHTML = jobtypename;
    cell4.innerHTML = hours_perweekname;
    cell5.innerHTML = "";

    $("#hours_perweek").val('default');
    $("#hours_perweek").selectpicker("refresh");
    $("#jobtype").val('default');
    $("#jobtype").selectpicker("refresh");
    $("#student").val('default');
    $("#student").selectpicker("refresh");
    $("#position").val('default');
    $("#position").selectpicker("refresh");

 // if Secondary option is selected, show primary supervisor selecpicker
    if(jobtypename == "Secondary"){
      $("#primary_table").show();
      var cell5 = row.insertCell(4);
      cell5.innerHTML = primary_supervisorname;
      $("#primary_supervisor").val('default');
      $("#primary_supervisor").selectpicker("refresh");
    }
}


// Pops up a modal for Seconday Postion
$('#jobtype').change(function(){
  //this is just getting the value that is selected
  var jobtype = $(this).val();
  if (jobtype == "Secondary") {
      $('#SecondaryModal').modal('show');
  }

});

// Pops up a modal for overload
$('#hours_perweek').change(function(){
  //this is just getting the value that is selected
  var hour = $(this).val();
  if (hour == "20") {
      $('#OverloadModal').modal('show');
  }

});

function Refresh() {
        window.parent.location = window.parent.location.href;
    }
