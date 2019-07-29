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
$("#plus").hide();
$("#mytable").hide();

function fill_dates(response){
  for (var key in response){
    $("#datetimepicker1").val(response[key]["Start Date"]);
    $("#datetimepicker2").val(response[key]["End Date"]);
  }
}

function prefilleddate(obj){
  var termcode = obj.value
  $.ajax({
    url: "/laborstatusform/getDate/" + termcode,
    dataType: "json",
    success: function (response){
       fill_dates(response)
    }
  })
}

function show_access_level(obj){
  $("#ContractHours").hide();
  $("#Hours_PerWeek").hide();
  $("#JopTypes").hide();
  $("#Student").hide();
  $("#Position").hide();
  $("#plus").hide();
  var termcode = obj.value;
  var whichterm = termcode.toString().substr(-2);
  if (whichterm != 11 && whichterm !=12 && whichterm !=00) { // Summer term or any other break period
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

function fill_positions(response) {
  var selected_positions = document.getElementById("position");
  if (selected_positions){
    $("#position").empty();
    for (var key in response) {
      var options = document.createElement("option");
      options.text = response[key]["position"].toString() + " " + "(" + response[key]["WLS"].toString() + ")"
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

// TABLE
function displayTable() {
  $("#mytable").show();
  $("#job_table").hide();
  $("#hours_table").hide();
  $("#primary_table").hide();
  $("#contract_table").hide();
  var termcode = $('#term').val();
  var whichterm = termcode.toString().substr(-2);
  if (whichterm != 11 && whichterm !=12 && whichterm !=00) {
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
          return;
          }
       if ((td0.innerHTML == studentname) && (td2.innerHTML == "Secondary") && (td1.innerHTML == positionname)) {

          category = "danger";
          msg = `Match found for ${studentname} , ${positionname} and Secondary. Insert rejected`;
          $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>');
          $("#flasher").delay(4000).fadeOut();
          $("#job_table").show();
          $("#hours_table").show();
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
  var studentname = student.options[student.selectedIndex].text;
  var position = document.getElementById("position");
  var positionname = position.options[position.selectedIndex].text;
  var posn_code = $("#position").val()
  var contracthoursname = document.getElementById("contracthours").value;
 // Summer term or any other break period
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  $(cell2).attr("data-posn", posn_code);
  cell2.id="position_code";
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

function getprimarysupervisor(){
  var student = $("#student").val();
  var term = $("#term").val();
  var url = "/laborstatusform/getstudents/" + term +"/" +student;
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      $("#job_table").show();
      $("#hours_table").show();
      var result = $.isEmptyObject(response);
      if (result) {
        $('#NoPrimaryModal').modal('show');
      }
      else {
          $('#PrimaryModal').modal('show');
          create_and_fill_table()
      }
    }
  });
}

function create_and_fill_table() {
  var table = document.getElementById("mytable");
  var student = document.getElementById("student");
  var studentname = student.options[student.selectedIndex].text;
  var position = document.getElementById("position");
  var positionname = position.options[position.selectedIndex].text;
  var posn_code = $("#position").val()
  var jobtype = document.getElementById("jobtype");
  var jobtypename = jobtype.options[jobtype.selectedIndex].text;
  var hours_perweek = document.getElementById("hours_perweek");
  var hours_perweekname = hours_perweek.options[hours_perweek.selectedIndex].text;

  $("#mytable").show();
  $("#job_table").show();
  $("#hours_table").show();
  $("#primary_table").hide();
  $("#contract_table").hide();
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);

  cell1.innerHTML = studentname;
  cell2.innerHTML = positionname;
  $(cell2).attr("data-posn", posn_code);
  cell2.id="position_code";
  cell3.innerHTML = jobtypename;
  cell4.innerHTML = hours_perweekname;

  $("#hours_perweek").val('default');
  $("#hours_perweek").selectpicker("refresh");
  $("#jobtype").val('default');
  $("#jobtype").selectpicker("refresh");
  $("#student").val('default');
  $("#student").selectpicker("refresh");
  $("#position").val('default');
  $("#position").selectpicker("refresh");
}

function CheckAcademicYear() {
    var jobtype = document.getElementById("jobtype");
    var jobtypename = jobtype.options[jobtype.selectedIndex].text;
    if (jobtypename == "Secondary") {
      getprimarysupervisor()
    }
    else{
      create_and_fill_table()
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

function disableTerm() {
  $("#term").prop("disabled", "disabled");
}

function userInsert(){

  var list_dict_ajax = [];
  $('#mytable tr').has('td').each(function() {

      supervisor = $("#supervisor").val();
      department = $("#department").val();
      term = $("#term").val();
      var whichterm = term.toString().substr(-2);
      startdate = $("#datetimepicker1").val();
      enddate = $("#datetimepicker2").val();
      var posn_code = $("#position_code").attr("data-posn");
      list_dict = []
      list_dict.push(supervisor, department, term, startdate, enddate, posn_code)
      var headers_label = ["Supervisor", "Department", "Term", "Start Date", "End Date", "Position Code"]
      var tabledata_dict = {};
      for (i in list_dict) {
        tabledata_dict[headers_label[i]] = list_dict[i];
      }
      if (whichterm != 11 && whichterm !=12 && whichterm !=00) {
        tabledata_dict["Job Type"] = "Secondary";
        var headers_2_data = ["Student", "Position", "Contract Hours"];
        $('td', $(this)).each(function(index, item) {
          tabledata_dict[headers_2_data[index]] = $(item).html();
        });
        list_dict_ajax.shift();
        list_dict_ajax.push(tabledata_dict);
        test_dict = {}
        for ( var key in list_dict_ajax){
          test_dict[key] = list_dict_ajax[key];
        }
      }
      else {
          var headers_data = ["Student", "Position", "Job Type", "Hours Per Week"];
          $('td', $(this)).each(function(index, item) {
            tabledata_dict[headers_data[index]] = $(item).html();
          });
          list_dict_ajax.shift();
          list_dict_ajax.push(tabledata_dict);
          test_dict = {}
          for ( var key in list_dict_ajax){
            test_dict[key] = list_dict_ajax[key];
          }
      }
    });
  data = JSON.stringify(test_dict);
  $.ajax({
         method: "POST",
         url: '/laborstatusform/userInsert',
         data: data,
         contentType: 'application/json',
         success: function(response) {
             if (response["Success"]) {
               msg = "Labor Status form has been created.";
               category = "info";
               $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>');
               $("#flasher").delay(4000).fadeOut();
               return;
             }
           }
         });
       }
