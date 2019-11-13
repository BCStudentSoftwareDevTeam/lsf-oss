var globalArrayOfStudents = [];
var display_failed = [];

$(document).ready(function(){
    $("[data-toggle=\"tooltip\"]").tooltip();
    $( "#dateTimePicker1, #dateTimePicker2" ).datepicker();
    if($("#selectedDepartment").val()){ // prepopulates position on redirect from rehire button and checks whether department is in compliance.
      checkCompliance($("#selectedDepartment"));
      getDepartment($("#selectedDepartment"), "stopSelectRefresh");
    }
    if($("#jobType").val()){ // fills hours per week selectpicker with correct information from laborstatusform. This is triggered on redirect from form history.
      var value = $("#selectedHoursPerWeek").val();
      $("#selectedHoursPerWeek").val(value);
      fillHoursPerWeek("fillhours");
    }
    console.log(display_failed.length);
});

$("laborStatusForm").submit(function(event) {
  event.preventDefault();
});

$(document).on("keyup", "input[name=contractHours]", function () { // sets contract hours minimum value
   var _this = $(this);
   var min = parseInt(_this.attr("min")) || 1; // if min attribute is not defined, 1 is default
   var val = parseInt(_this.val()) || (min - 1); // if input char is not a number the value will be (min - 1) so first condition will be true
   if(val < min) {
       _this.val( min );
     }
});

$("#jobType").change(function(){ // Pops up a modal for Seconday Postion
  //this is just getting the value that is selected
  var jobType = $(this).val();
  if (jobType == "Secondary") {
      $("#warningModal").modal("show");
      $("#warningModalTitle").html("Warning") //Maybe change the wording here.
      $("#warningModalText").html("The labor student and the supervisor of this secondary position should obtain permission from the primary supervisor before submitting this labor status form.");
      $("#warningModal").on("hidden.bs.modal", function(){
      $("#warningModalText").html("");
      $("#warningModalTitle").html("Insert Rejected") //Maybe change the wording here.
      //Testing out modal stuff here
      });
    }
  });

function disableTermSupervisorDept() {
  // disables term, supervisor and department select pickers when add student button is clicked
  $("#selectedTerm").prop("disabled", "disabled");
  $("#termInfo").show();
  $("#selectedTerm").selectpicker("refresh");
  $("#selectedSupervisor").prop("disabled", "disabled");
  $("#supervisorInfo").show();
  $("#selectedSupervisor").selectpicker("refresh");
  $("#selectedDepartment").prop("disabled", "disabled");
  $("#departmentInfo").show();
  $("#selectedDepartment").selectpicker("refresh");
}

function preFilledDate(obj){ // get term start date and end date
  var termCode = $(obj).val();
  $.ajax({
    url: "/laborstatusform/getDate/" + termCode,
    dataType: "json",
    success: function (response){
       fillDates(response);
    }
  });
}

function fillDates(response) { // prefill term start and term end
  for (var key in response){
    var start = response[key]["Start Date"];
    var end = response[key]["End Date"];
    // Start Date
    var startd = new Date(start);
    var dayStart1 = startd.getDate();
    var monthStart1 = startd.getMonth();
    var yearStart = startd.getFullYear();
    // End Date
    var endd = new Date(end);
    var dayEnd1 = endd.getDate();
    var monthEnd1 = endd.getMonth();
    var yearEnd = endd.getFullYear();
    // Pre-populate values
    $("#dateTimePicker1").val(start);
    $("#dateTimePicker2").val(end);
    // set the minimum and maximum Date for Term Start Date
    $("#dateTimePicker1").datepicker({minDate: new Date(yearStart, monthStart1, dayStart1)});
    $("#dateTimePicker1").datepicker({maxDate: new Date(yearEnd, monthEnd1, dayEnd1)});
    $("#dateTimePicker1").datepicker("option", "minDate", new Date(yearStart, monthStart1, dayStart1));
    $("#dateTimePicker1").datepicker("option", "maxDate", new Date(yearEnd, monthEnd1, dayEnd1));
    // set the minimum and maximum Date for Term End Date
    $("#dateTimePicker2").datepicker({maxDate: new Date(yearEnd, monthEnd1, dayEnd1)});
    $("#dateTimePicker2").datepicker({minDate: new Date(yearStart, monthStart1, dayStart1)});
    $("#dateTimePicker2").datepicker("option", "maxDate", new Date(yearEnd, monthEnd1, dayEnd1));
    $("#dateTimePicker2").datepicker("option", "minDate", new Date(yearStart, monthStart1, dayStart1));
  }
}

function updateDate(obj) { // updates max and min dates of the datepickers as the other datepicker changes
  var dateToChange = new Date($(obj).val());
  var newMonth = dateToChange.getMonth();
  var newYear = dateToChange.getFullYear();
  if(obj.id == "dateTimePicker2"){
    var newDay = dateToChange.getDate() - 1;
    $("#dateTimePicker1").datepicker({maxDate: new Date(newYear, newMonth, newDay)});
    $("#dateTimePicker1").datepicker("option", "maxDate", new Date(newYear, newMonth, newDay));
  }
  if(obj.id == "dateTimePicker1"){
    var newDay = dateToChange.getDate() + 1;
    $("#dateTimePicker2").datepicker({minDate: new Date(newYear, newMonth, newDay)});
    $("#dateTimePicker2").datepicker( "option", "minDate", new Date(newYear, newMonth, newDay));
  }
}

function getDepartment(object, stopSelectRefresh="") { // get department from select picker
   var department = $(object).val();
   var url = "/laborstatusform/getPositions/" + department;
       $.ajax({
         url: url,
         dataType: "json",
         success: function (response){
            fillPositions(response, stopSelectRefresh);
          }
        });
  }

 function fillPositions(response, stopSelectRefresh="") { // prefill Position select picker with the positions of the selected department
   var selectedPositions = $("#position");
   $("#position").empty();
   for (var key in response) {
     selectedPositions.append(
       $("<option />")
          .text(response[key].position+ " " + "(" + response[key].WLS+ ")")
          .attr("id", key)
          .attr("data-wls", response[key].WLS)
     );
   }
   if (stopSelectRefresh== "") {
     $(".selectpicker").selectpicker("refresh");
   }
   else {
     value = $("#position").val();
     $("#position").val(value);
   }
 }

 // Pops up a modal for WLS 5, 6 or more
 $("#position").change(function(){
   //this is just getting the value that is selected
   var wls = $("#position").find("option:selected").attr("data-wls");
   if (wls >= 5) {
     $("#WLSModalTitle").html("Work-Learning-Service Levels (WLS)");
     $("#WLSModalText").html("Student with WLS Level 5 or 6 must have at least a 15 hour contract. " +
                              "These positions require special authorization as specified at " +
                              "<a href=\"http://catalog.berea.edu/2014-2015/Tools/Work-Learning-Service-Levels-WLS\""+
                              "target=\"_blank\">The Labor Program Website.</a>");
     $("#WLSModal").modal("show");
 }
});

 function fillHoursPerWeek(fillhours=""){ // prefill hours per week select picker
  var selectedHoursPerWeek = $("#selectedHoursPerWeek");
  var jobType = $("#jobType").val();
  if (selectedHoursPerWeek){
    $("#selectedHoursPerWeek").empty();
    var list = ["10", "15", "20"];
    if (jobType == "Secondary"){
       list = ["5", "10"];
    }
    $(list).each(function(i,hours) {
      selectedHoursPerWeek.append($("<option />").text(hours));
    });
  }
    if (fillhours == ""){
      $(".selectpicker").selectpicker("refresh");
    }
  }

// checks if wls is greater than 5
function checkWLS() {
  var wls = $("#position").find("option:selected").attr("data-wls");
  var hoursPerWeek = $("#selectedHoursPerWeek").val();

  if (wls >= 5 && hoursPerWeek < 15 ) {
    $("#WLSModalTitle").html("Insert Rejected");  // FIXME: Maybe change Modal title (ask Scott)
    $("#WLSModalText").html("Student requires at least a 15 hour contract with positions WLS 5 or greater."); // FIXME Maybe change modal Language (ask Scott)
    $("#WLSModal").modal("show");
    return false;
  }
  else {
    return true;
  }
}

function checkJobType() {
  // This function checks the job type selected along with the WLS of the position.
  // If the job type is secondary and the WLS is 5 or 6, it rejects the insert.
  var jobTypeSelected = $('#jobType').find('option:selected').attr('data-jobType');
  var wlsSelected = $('#position').find('option:selected').attr('data-wls');
  if (jobTypeSelected == "Secondary" && wlsSelected >=5) {
    $('#WLSModalTitle').html("Insert Rejected");
    $('#WLSModalText').html("Position with WLS 5 or 6 cannot be a secondary position.");
    $('#WLSModal').modal('show');
    return false;
  }
  else {
    return true;
  }
}

// Check if department is in compliance.
function checkCompliance(obj) {
  var department = $(obj).val();
  var url = "/laborstatusform/getcompliance/" + department;
      $.ajax({
        url: url,
        dataType: "json",
        success: function (response){
          if(response.Department["Department Compliance"] == false){
            $("#OutofComplianceModal").modal("show");
            $(".disable").prop("disabled", true);
            $("#selectedTerm").selectpicker("refresh");
            $("#student").selectpicker("refresh");
            $("#position").selectpicker("refresh");
            $("#selectedSupervisor").selectpicker("refresh");
            $("#selectedDepartment").selectpicker("refresh");
          }
          else{
            $(".disable").prop("disabled", false);
          }
        }
      });
}

//refresh select pickers
function refreshSelectPickers() {
  $("#selectedContractHours").val("");
  $("#selectedHoursPerWeek").val("default");
  $("#selectedHoursPerWeek").selectpicker("refresh");
  $("#jobType").val("default");
  $("#jobType").selectpicker("refresh");
  $("#student").val("default");
  $("#student").selectpicker("refresh");
  $("#position").val("default");
  $("#position").selectpicker("refresh");
}

// TABLE LABELS
$("#contractHours").hide();
$("#hoursPerWeek").hide();
$("#JopTypes").hide();
$("#plus").hide();
$("#mytable").hide();
$("#failedTable").hide();
function showAccessLevel(obj){ // Make Table labels appear
  $("#contractHours").hide();
  $("#hoursPerWeek").hide();
  $("#JopTypes").hide();
  $("#plus").hide();
  var termCode = $(obj).val();
  var whichTerm = termCode.substr(-2);
  if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00) { // Summer term or any other break period table labels
    $("#contractHours").show();
    $("#plus").show();
  }
  else{ // normal semester like Fall or Spring table labels
    $("#hoursPerWeek").show();
    $("#JopTypes").show();
    $("#plus").show();
  }
}
// TABLE LABELS

// hide review button will show when add student is clicked
$("#reviewButton").hide();
//end

// Table glyphicons
function showNotesModal(glyphicon){// pops up Note Modal when notes glyphicon is clicked
  var rowParent = glyphicon.parentNode.parentNode;
  var table = document.getElementById("mytable").getElementsByTagName("tbody")[0];
  for (var i = 0, row; row = table.rows[i]; i++) {
    if (rowParent === table.rows[i]) {
      $("#modal_text").val(globalArrayOfStudents[i].stuNotes);
      $("#saveButton").attr("onclick","saveNotes(\"" + i +"\")");
      break;
    }
  }
  $("#noteModal").modal("show");
}

function saveNotes(arrayIndex){ // saves notes written in textarea when save button of modal is clicked
  if($("#modal_text").val() != ""){
    globalArrayOfStudents[arrayIndex].stuNotes = $("#modal_text").val();
  }
}

function deleteRow(glyphicon) {
  var rowParent = glyphicon.parentNode.parentNode;
  var table = document.getElementById("mytable").getElementsByTagName("tbody")[0];
  for (var i = 0, row; row = table.rows[i]; i++) {
    if (rowParent === table.rows[i]) {
      $(glyphicon).parents("tr").remove();
      globalArrayOfStudents.splice(i, 1);
      break;
    }
  }
}
//END of glyphicons

function errorFlash(){
  category = "danger";
  msg = "Please fill out all fields before submitting.";
  $("#flash_container").prepend("<div class=\"alert alert-"+ category +"\" role=\"alert\" id=\"flasher\">"+msg+"</div>");
  $("#flasher").delay(3000).fadeOut();
}

// TABLE
function displayTable() { // displays table when plus glyphicon is clicked and check if fields are filled out
  var studentDict = createStuDict();
  console.log("$$$$$$ : ", studentDict)
  if (studentDict === false) {
    console.log("studentDict returned false")
    errorFlash();
  }
  else  {
    console.log("going into checkPrimaryPosition")
    checkPrimaryPosition(studentDict);
     }
  }

function createStuDict(){
  var supervisor = $("#selectedSupervisor").find("option:selected").text();
  var supervisorID = $("#selectedSupervisor").find("option:selected").attr("value");
  var department = $("#selectedDepartment").find("option:selected").text();
  var termCodeSelected = $("#selectedTerm").find("option:selected").attr("data-termCode");
  var termCodeLastTwo = termCodeSelected.slice(-2);
  var studentName = $("#student option:selected" ).text();
  if (!studentName){
    return false;
  }
  var positionName = $("#position option:selected").text();
  // if (!positionName){
  //   return false;
  // }
  var positionCode = $("#position").find("option:selected").attr("id");
  var wls = $("#position").find("option:selected").attr("data-wls");
  var studentBNumber = $("#student").val();
  var startDate  = $("#dateTimePicker1").datepicker({dateFormat: "dd-mm-yy"}).val();
  var endDate  = $("#dateTimePicker2").datepicker({dateFormat: "dd-mm-yy"}).val();
  if (termCodeLastTwo == "11" || termCodeLastTwo == "12" || termCodeLastTwo == "00"){
    var jobType = $("#jobType");
    var jobTypeName = $("#jobType option:selected").text();
    var hoursPerWeek = $("#selectedHoursPerWeek");
    var hoursPerWeekName = $("#selectedHoursPerWeek :selected").val();
    if (!hoursPerWeekName){
      return false;
      }
    }
  else {
    var jobTypeName = "Secondary";
    var selectedContractHoursName = $("#selectedContractHours").val();
    if (selectedContractHoursName === ""){
        return false;
      }
    }
  var studentDict = {stuName: studentName,
                    stuBNumber: studentBNumber,
                    stuPosition: positionName,
                    stuPositionCode: positionCode,
                    stuJobType: jobTypeName,
                    stuWeeklyHours: parseInt(hoursPerWeekName, 10),
                    stuContractHours: parseInt(selectedContractHoursName, 10),
                    stuWLS: wls,
                    stuStartDate: startDate,
                    stuEndDate: endDate,
                    stuTermCode: termCodeSelected,
                    stuNotes: null,
                    stuSupervisor: supervisor,
                    stuDepartment: department,
                    stuSupervisorID: supervisorID
                    };
    return studentDict;
  }

function checkDuplicate(studentDict) {// checks for duplicates in the table. This is for Academic Year
  for(i = 0; i < globalArrayOfStudents.length; i++){
    if(globalArrayOfStudents[i].stuName == studentDict.stuName &&
      globalArrayOfStudents[i].stuJobType == studentDict.stuJobType &&
      (studentDict.stuJobType == "Primary" || globalArrayOfStudents[i].stuPosition == studentDict.stuPosition)){
      $("#warningModalText").html("Match found for " + studentDict.stuName +"'s " + studentDict.stuJobType +" position.");
      $("#warningModal").modal("show");
      return false;
    }
  }
  return true;
}

function checkPrimaryPosition(studentDict){
  var termCodeLastTwo = (studentDict).stuTermCode.slice(-2);
  var term = $("#selectedTerm").val();
  var url = "/laborstatusform/getstudents/" + term +"/" +studentDict.stuBNumber;
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      console.log(response);
      console.log("post response");
      console.log(studentDict);
      console.log(Object.keys(response).length);
      if(Object.keys(response).length > 0) {
        if (studentDict.stuJobType == "Primary"){
          console.log("Adding Primary with Primary in database");
          $("#warningModalText").html(studentDict.stuName + " already has a primary position.");
          $("#warningModal").modal("show");
        }
        else if(studentDict.stuJobType == "Secondary"){
          console.log("Adding Secondary with Primary in database");
          if (checkDuplicate(studentDict) == true && checkTotalHours(studentDict, response) == true) {
            createAndFillTable(studentDict);
          }
          else {
            console.log("This is a duplicate");
            $("#warningModalText").html("Match found for " + studentDict.stuName + "'s " + studentDict.stuJobType + " position.");
            $("#warningModal").modal("show");
          }
        }
      }
      else {
        if(studentDict.stuJobType == "Primary"){
          console.log("Adding Primary without Primary in database");
          if (checkDuplicate(studentDict) == true  && checkTotalHours(studentDict, response) == true){
            createAndFillTable(studentDict);
          }
          else {
            console.log("This is a duplicate");
            $("#warningModalText").html("Match found for " + studentDict.stuName + "'s " + studentDict.stuJobType + " position.");
            $("#warningModal").modal("show");
          }
        }
        else {
          if (termCodeLastTwo == "11" || termCodeLastTwo == "12" || termCodeLastTwo == "00"){
            console.log("Adding Secondary without Primary in database");
            $("#warningModalText").html(studentDict.stuName + " needs an approved primary position before a secondary position can be added.");
            $("#warningModal").modal("show");
          }
          else {
            if (checkDuplicate(studentDict) == true && checkTotalHours(studentDict, response) == true){
              createAndFillTable(studentDict);
            }
            else {
              console.log("This is a duplicate");
              $("#warningModalText").html("Match found for " + studentDict.stuName + "'s " + studentDict.stuJobType + " position.");
              $("#warningModal").modal("show");
            }
          }
        }
      }
    }
  });
}
function createAndFillTable(studentDict) {
  globalArrayOfStudents.push(studentDict);
  console.log(globalArrayOfStudents);
  $("#mytable").show();
  $("#jobTable").show();
  $("#hoursTable").show();
  var termCodeLastTwo = (studentDict).stuTermCode.slice(-2);
  var table = document.getElementById("mytable").getElementsByTagName("tbody")[0]; //This one needs document.getElementById, it won't work without it
  if (termCodeLastTwo == "11" || termCodeLastTwo == "12" || termCodeLastTwo == "00") {
    var notesID0 = String((studentDict).stuName + (studentDict).stuJobType + (studentDict).stuPosition);
    var notesID1 = notesID0.replace(/ /g, "");
    var notesID2 = notesID1.substring(0, notesID1.indexOf("("));
  }
  else {
    var selectedContractHoursName = $("#selectedContractHours").val();// For whatever reason this is undefined
  }
  var notesGlyphicon = "<a data-toggle=\"modal\" onclick = \"showNotesModal(this)\" id= \""+notesID2+
                                                          "\" ><span class=\"glyphicon glyphicon-edit\"></span></a>";
  var removeIcon = "<a onclick= \"deleteRow(this)\"><span class=\"glyphicon glyphicon-remove\"></span></a>";
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);
  var cell5 = row.insertCell(4);
  var cell6 = row.insertCell(5);
  var cell7 = row.insertCell(6);
  $(cell1).html((studentDict).stuName + " " + "(" + (studentDict).stuBNumber+ ")");
  $(cell2).html((studentDict).stuPosition);
  $(cell2).attr("data-posn", (studentDict).stuPositionCode);
  $(cell2).attr("data-wls", (studentDict).stuWLS);
  cell2.id="position_code";
  if (termCodeLastTwo == "11" || termCodeLastTwo == "12" || termCodeLastTwo == "00") {
    $(cell3).html((studentDict).stuJobType);
    $(cell4).html((studentDict).stuWeeklyHours);
    $(cell5).html((studentDict).stuStartDate + " - " + (studentDict).stuEndDate);
    $(cell6).html(notesGlyphicon);
    $(cell7).html(removeIcon);
  }
  else {
    console.log(selectedContractHoursName);
    $(cell3).html("Secondary");
    $(cell4).html(selectedContractHoursName);
    $(cell5).html((studentDict).stuStartDate + " - " + (studentDict).stuEndDate);
    $(cell6).html(notesGlyphicon);
    $(cell7).html(removeIcon);
  }
  refreshSelectPickers();
  var rowLength = document.getElementById("mytable").rows.length;
  if (rowLength > 1) {
    $("#reviewButton").show();
  }
}

function checkTotalHours(studentDict, databasePositions) {// gets sum of the total weekly hours from the database and add it to the ones in the table.
  totalHoursCount = studentDict.stuWeeklyHours;
  for (i = 0; i < globalArrayOfStudents.length; i++){
    if (globalArrayOfStudents[i].stuName == studentDict.stuName){
      console.log(totalHoursCount);
      totalHoursCount = totalHoursCount + globalArrayOfStudents[i].stuWeeklyHours;
    }
  }
  for (i = 0; i < databasePositions.length; i++){
    totalHoursCount = totalHoursCount + databasePositions[i].weeklyHours;
  }
  if (totalHoursCount > (15)){
    // TODO: Show modal saying they have too many hours
    $('#OverloadModal').modal('show');
    $('#overloadModalButton').attr('data-target', '#PrimaryModal');
    // $('#OverloadModal').on('hidden.bs.modal', function() {
    // $('#PrimaryModal').modal('show');
    //return false
  }
  return true;
}

function reviewButtonFunctionality() { // Triggred when Review button is clicked and checks if fields are filled out.
  disableTermSupervisorDept();
  var rowLength = document.getElementById("mytable").rows.length;
  if (rowLength > 1) {
     createModalContent();
  }
}

function createModalContent() { // Populates Submit Modal with Student information from the table
  term = $("#selectedTerm").val();
  var whichTerm = term.toString().substr(-2);
  modalList = [];
  if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
    for (var i = 0; i < globalArrayOfStudents.length; i++) {
      var bigString = "<li>" + globalArrayOfStudents[i].stuName + " | " + globalArrayOfStudents[i].stuPosition + " | " +
                      globalArrayOfStudents[i].stuContractHours + " hours";
      modalList.push(bigString);
    }
    $("#SubmitModalText").html("Labor status form(s) will be submitted for:<br><br>" +
                                                            "<ul style=\"display:inline-block;text-align:left;\">" +
                                                            modalList.join("</li>")+"</ul>"+
                                                            "<br><br>The labor status form will be eligible for approval in one business day.");
    $("#SubmitModal").modal("show");
  }
  else {
    for (var i = 0; i < globalArrayOfStudents.length; i++) {
      var bigString = "<li>" + globalArrayOfStudents[i].stuName + " | " + globalArrayOfStudents[i].stuPosition +
                      " | " + globalArrayOfStudents[i].stuJobType + " | " + globalArrayOfStudents[i].stuWeeklyHours + " hours";
      modalList.push(bigString);
    }
    $("#SubmitModalText").html("Labor status form(s) will be submitted for:<br><br>" +
                               "<ul style=\"display: inline-block;text-align:left;\">" +
                               modalList.join("</li>")+"</ul>"+
                               "<br><br>The labor status form will be eligible for approval in one business day.");
    $("#SubmitModal").modal("show");
  }
}

// SEND DATA TO THE DATABASE
function userInsert(){
  $("#laborStatusForm").on("submit", function(e) {
    e.preventDefault();
  });
  $.ajax({
         method: "POST",
         url: "/laborstatusform/userInsert",
         data: JSON.stringify(globalArrayOfStudents),
         contentType: "application/json",
         success: function(response) {
           console.log("response from userInsert : ", response)
           term = $("#selectedTerm").val();
           var whichTerm = parseInt(term.toString().substr(-2));
           console.log(typeof(whichTerm));
           modalList = [];
           for(var key = 0; key < globalArrayOfStudents.length; key++){
             var studentName = globalArrayOfStudents[key].stuName;
             var position = globalArrayOfStudents[key].stuPosition;
             var selectedContractHours = globalArrayOfStudents[key].stuContractHours;
             var jobType = globalArrayOfStudents[key].stuJobType;
             var hours = globalArrayOfStudents[key].stuWeeklyHours;
             var selectedContractHours = globalArrayOfStudents[key].stuWeeklyHours;
             console.log(globalArrayOfStudents);
             if (response[key] === true){
               console.log("response is true")
               if (whichTerm !== 11 && whichTerm !==12 && whichTerm !==00){
                 var bigString = "<li>" +"<span class=\"glyphicon glyphicon-ok\" style=\"color:green\"></span> " + studentName + " | " + position + " | " + selectedContractHours + " hours";
               }
               else {
                 var bigString = "<li>"+"<span class=\"glyphicon glyphicon-ok\" style=\"color:green\"></span> " + studentName + " | " + position + " | " + jobType + " | " + hours + " hours";
               }
             }
             else {
               if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
                 display_failed.push(key);
                 console.log("key",key);
                 var bigString = "<li>" +"<span class=\"glyphicon glyphicon-remove\" style=\"color:red\"></span> " + studentName + " | " + position + " | " + selectedContractHours + " hours";
               }
               else {
                 console.log("key",key);
                 console.log("sksksk");
                 display_failed.push(key);
                 var bigString = "<li>"+"<span class=\"glyphicon glyphicon-remove\" style=\"color:red\"></span> " + studentName + " | " + position + " | " + jobType + " | " + hours + " hours";
               }
             }
             modalList.push(bigString);
           }


         $("#SubmitModalText").html("Labor status form(s) will be submitted for:<br><br>" +
                                    "<ul style=\"list-style-type:none; display: inline-block;text-align:left;\">" +
                                     modalList.join("</li>")+"</ul>"+
                                    "<br><br>The labor status form will be eligible for approval in one business day.");
         $("#SubmitModal").modal("show");
       }
     });
     $("#SubmitModal").modal({backdrop: true, keyboard: false, show: true});
     $("#SubmitModal").data("bs.modal").options.backdrop = "static";
     $("#submitmodalid").html("Done");


     // $("#submitmodalid").attr("onclick", function() { window.location.replace("/laborstatusform");});
       document.getElementById("submitmodalid").onclick = function() {
         if (display_failed.length > 0){
           $('#tbodyid').empty();
           // $('#reviewButton').hide();
           // $('#failedTable').show();
           for (var i = 0; i < display_failed.length; i++){
             // console.log('indiviual failed form', globalArrayOfStudents[display_failed[i]]);
             if (globalArrayOfStudents[display_failed[i]].stuContractHours){
               globalArrayOfStudents[display_failed[i]].stuWeeklyHours = '';
             }
             else{
               globalArrayOfStudents[display_failed[i]].stuContractHours = '';
             }
             $('#mytable').append('<tr>'+
                                      '<td>'+ globalArrayOfStudents[display_failed[i]].stuName+'</td>'+
                                      '<td>'+ globalArrayOfStudents[display_failed[i]].stuPosition+'</td>'+
                                      '<td>'+ globalArrayOfStudents[display_failed[i]].stuJobType+'</td>'+
                                      '<td>'+ globalArrayOfStudents[display_failed[i]].stuWeeklyHours + globalArrayOfStudents[display_failed[i]].stuContractHours+'</td>'+
                                      '<td>'+ globalArrayOfStudents[display_failed[i]].stuStartDate + '-'+ globalArrayOfStudents[display_failed[i]].stuEndDate+'</td>'+
                                      '<td>'+ globalArrayOfStudents[display_failed[i]].stuNotes+'</td>'+
                                      '</tr>');
           }
           $('#SubmitModal').modal("hide");
           $("#SubmitModal").modal({backdrop: false, keyboard: true, show: false});
           $("#SubmitModal").data("bs.modal").options.backdrop = true;
           $("#submitmodalid").html("submit");
         }
         else{
         window.location.replace("/laborstatusform");
       }
        }; // seems to be necessary to use this line to get it to work

     // for(var key = 0; key < display_failed.length; key++){
     //   $('#failedTable').html(globalArrayOfStudents[display_failed[key]][stuName]);
     // }
   }
