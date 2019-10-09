var globalArrayOfStudents = [];

$(document).ready(function(){
    $("[data-toggle=\"tooltip\"]").tooltip();
    $( "#dateTimePicker1, #dateTimePicker2" ).datepicker();

    if($("#selectedDepartment").val()){// prepopulates position on redirect from rehire button and checks whether department is in compliance.
      checkCompliance($("#selectedDepartment"));
      getDepartment($("#selectedDepartment"), "stopSelectRefresh");
    }

    if($("#jobType").val()){// fills hours per week selectpicker with correct information from laborstatusform. This is triggered on redirect from form history.
      var value = $("#selectedHoursPerWeek").val();
      $("#selectedHoursPerWeek").val(value);
      fillHoursPerWeek("fillhours");
    }
});

$("laborStatusForm").submit(function(event) {
  event.preventDefault();
});

$(document).on("keyup", "input[name=contractHours]", function () { // sets contract hours minimum value
   var _this = $(this);
   var min = parseInt(_this.attr("min")) || 1; // if min attribute is not defined, 1 is default
   var val = parseInt(_this.val()) || (min - 1); // if input char is not a number the value will be (min - 1) so first condition will be true
   if(val < min)
       _this.val( min );
});

// Pops up a modal for Seconday Postion
$("#jobType").change(function(){
  //this is just getting the value that is selected
  var jobType = $(this).val();
  if (jobType == "Secondary") {
      $("#SecondaryModal").modal("show");
  }
});

// Pops up a modal for overload
$("#selectedHoursPerWeek").change(function(){
  //this is just getting the value that is selected
  var hour = $(this).val();
  if (hour == "20") {
      $("#OverloadModal").modal("show");
      $("#overloadModalButton").attr("data-target", ""); // prevent a Primary Modal from showing up
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

function fillDates(response){ // prefill term start and term end
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

    /*Here is the code to start with for restricting dates for the datepicker when it is not readonly.  Right now it restricts dates when you type
    them in and hit enter, not if you just type them in and tab over to the next selectpicker.  Right now the datepickers are readonly.*/

    // var dayStart2 = ("0" + (startd.getDate())).slice(-2);
    // var monthStart2 = ("0" + (startd.getMonth() + 1)).slice(-2);
    // var dayEnd2 = ("0" + (endd.getDate())).slice(-2);
    // var monthEnd2 = ("0" + (endd.getMonth() + 1)).slice(-2);
    // $("#dateTimePicker2").attr("min", monthStart2 + "-" + dayStart2 + "-" + yearStart);
    // $("#dateTimePicker2").attr("max", monthEnd2 + "-" + dayEnd2 + "-" + yearEnd);
    // $("#dateTimePicker1").attr("min", monthStart2 + "-" + dayStart2 + "-" + yearStart);
    // $("#dateTimePicker1").attr("max", monthEnd2 + "-" + dayEnd2 + "-" + yearEnd);
    // $("#dateTimePicker1").datepicker("refresh");
    // $("#dateTimePicker2").datepicker("refresh");
  }
}

function updateDate(obj){ // updates the max date of the start datepicker to not be after what the end datePicker picked
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
function showNotesModal(obj){// pops up Note Modal when notes glyphicon is clicked
  $("modal_text").val($("#"+obj).attr("data-note"));
  $("#saveButton").attr("onclick","saveNotes(\"" + obj +"\")");
  $("#noteModal").modal("show");
}

function saveNotes(obj){ // saves notes written in textarea when save button of modal is clicked
  var notes = $("#modal_text").val();
  $("#"+obj).attr("data-note", notes);
}

function deleteRow(row) { // Deletes Row when remove glyphicon is clicked.
  $(row).parents("tr").remove();
  // TODO: Will we need to modify the global array at all when this is called as well?
}
//END of glyphicons

function fields_are_empty(id_list) { // Checks if selectpickers are empty
  empty_element = false;
  $.each(id_list, function(id) {
    value = $("#"+id).val();
    empty_element = (value=="" || value==null);
  });
  return empty_element;
}

function errorFlash(){
  category = "danger";
  msg = "Please fill out all fields before submitting.";
  $("#flash_container").prepend("<div class=\"alert alert-"+ category +"\" role=\"alert\" id=\"flasher\">"+msg+"</div>");
  $("#flasher").delay(3000).fadeOut();
}

// TABLE
function displayTable() { // displays table when plus glyphicon is clicked and check if fields are filled out
  var id_list = ["selectedSupervisor", "selectedDepartment","selectedTerm", "dateTimePicker1", "dateTimePicker2"];
  var studentDict = createStuDict();
  checkPrimaryPosition(studentDict);
  return;
  if (fields_are_empty(id_list)) {
    errorFlash();
  }
  else if (checkWLS()){
    var termCode = $("#selectedTerm").val();
    var whichTerm = termCode.toString().substr(-2);
    if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00) {
      id_list = ["student", "position", "selectedContractHours"];
      if (fields_are_empty(id_list)) {
        errorFlash();
      }
      else {
        checkDuplicate();
       }
      }
    else {
      id_list = ["student", "position", "jobType", "selectedHoursPerWeek"];
      if (fields_are_empty(id_list)) {
        errorFlash();
      }
      else {
        checkDuplicate();
        return;
      }
    }
  }
}
function createStuDict(){
  var termCodeSelected = $("#selectedTerm").find("option:selected").attr("data-termCode");
  var termCodeLastTwo = termCodeSelected.slice(-2);
  var student = $("student");
  var studentName = $("#student option:selected" ).text();
  var position = $("position");
  var positionName = $("#position option:selected").text();
  var positionCode = $("#position").find("option:selected").attr("id");
  var wls = $("#position").find("option:selected").attr("data-wls");
  var studentBNumber = $("#student").val();
  var startDate  = $("#dateTimePicker1").datepicker({dateFormat: "dd-mm-yy"}).val();
  var endDate  = $("#dateTimePicker2").datepicker({dateFormat: "dd-mm-yy"}).val();
  if (termCodeLastTwo == "11" || termCodeLastTwo == "12" || termCodeLastTwo == "00") {
    var jobType = $("jobType");
    var jobTypeName = $("#jobType option:selected").text();
    var hoursPerWeek = $("selectedHoursPerWeek");
    var hoursPerWeekName = $("#selectedHoursPerWeek option:selected").text();
  }
  else {
    var selectedContractHoursName = $("#selectedContractHours").val();
  }
  if (termCodeLastTwo == "11" || termCodeLastTwo == "12" || termCodeLastTwo == "00"){
    var studentDict ={stuName: studentName,
                      stuBNumber: studentBNumber,
                      stuPosition: positionName,
                      stuPositionCode: positionCode,
                      stuJobType: jobTypeName,
                      stuHours: hoursPerWeekName,
                      stuWLS: wls,
                      stuStartDate: startDate,
                      stuEndDate: endDate,
                      stuTermCode: termCodeSelected,
                      stuNotes: ""
                      };
  }
  else{
     //#TODO: Add student dictionary for breaks to the global array
    var studentDict ={stuName: studentName,
                      stuBNumber: studentBNumber,
                      stuPosition: positionName,
                      stuPositionCode: positionCode,
                      stuContractHours: selectedContractHoursName,
                      stuStartDate: startDate,
                      stuEndDate: endDate,
                      stuTermCode: termCodeSelected,
                      stuNotes: ""
                      };
  }
  return studentDict;
}

function checkDuplicate(studentDict) {// checks for duplicates in the table. This is for Academic Year
  for(i = 0; i < globalArrayOfStudents.length; i++){
    if(globalArrayOfStudents[i].stuName == studentDict.stuName &&
      globalArrayOfStudents[i].stuJobType == studentDict.stuJobType &&
      (studentDict.stuJobType == "Primary" || globalArrayOfStudents[i].stuPosition == studentDict.stuPosition)){
      //FIXME: Change this to JQuery
      $("warningModalText").innerHTML = "Match found for " + studentDict.stuName +"'s " + studentDict.stuJobType +" position.";
      $("#warningModal").modal("show");
      return false;
    }
  }
  return true;
}

function checkPrimaryPosition(studentDict){
  var termCodeLastTwo = (studentDict).stuTermCode.slice(-2);
  var term = $("#selectedTerm").val();
  var url = "/laborstatusform/getstudents/" + term +"/" +studentDict["stuBNumber"];
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      console.log(response);
      console.log("post response");
      console.log(studentDict);

      try {
        if (response["PrimarySupervisor"]["selectedJobType"] == "Primary" && studentDict["stuJobType"] == "Primary"){
          console.log("Adding Primary with Primary in database");
          /// TODO: Display modal saying student already has a primary postion
          $("warningModalText").innerHTML = studentDict['stuName'] + " aleady has a primary position."
          $("warningModal").modal("show");
        }
        else if(response["PrimarySupervisor"]["selectedJobType"] == "Primary" && studentDict["stuJobType"] == "Secondary"){
          console.log("Adding Secondary with Primary in database");
          if (checkDuplicate(studentDict) == true){
            createAndFillTable(studentDict);
          }
          else {
            console.log("This is a duplicate")
            $("warningModalText").innerHTML = "Match found for " + studentDict.stuName +"'s " + studentDict.stuJobType +" position."; //Is this right?  Should double check
            $("#warningModal").modal("show");
          }
        }
      }
      catch(e) {
        //console.log(e);
        if(studentDict["stuJobType"] == "Primary"){
          console.log("Adding Primary without Primary in database");
          if (checkDuplicate(studentDict) == true){
            createAndFillTable(studentDict);
          }
          else {
            console.log("This is a duplicate")
            $("warningModalText").innerHTML = "Match found for " + studentDict.stuName +"'s " + studentDict.stuJobType +" position."; //Is this right?  Should double check
            $("#warningModal").modal("show");
        }
      }
        else {
          if (termCodeLastTwo == "11" || termCodeLastTwo == "12" || termCodeLastTwo == "00"){
          console.log("Adding Secondary without Primary in database");
          $("warningModalText").innerHTML = studentDict['stuName'] + " needs a primary position before a secondary position can be added."
          $("warningModal").modal("show");
        }
        else {
          if (checkDuplicate(studentDict) == true){
            createAndFillTable(studentDict);
          }
          else {
            console.log("This is a duplicate")
            $("warningModalText").innerHTML = "Match found for " + studentDict.stuName +"'s " + studentDict.stuJobType +" position."; //Is this right?  Should double check
            $("#warningModal").modal("show");
        }
        }

        }
      }

    }
  });
}
function createAndFillTable(studentDict) {
  console.log(globalArrayOfStudents);
  console.log("Filling table"); // fills the table.
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
    var selectedContractHoursName = $("#selectedContractHours"); // For whatever reason this is undefined
  }
  var notesGlyphicon = "<a data-toggle=\"modal\" onclick = \"showNotesModal(\""+notesID2+"\")\" id= \""+notesID2+
                                                          "\" ><span class=\"glyphicon glyphicon-edit\"></span></a>";
  var removeIcon = "<a onclick = \"deleteRow(this)\" class=\"remove\"><span class=\"glyphicon glyphicon-remove\"></span></a>";
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);
  var cell5 = row.insertCell(4);
  var cell6 = row.insertCell(5);
  var cell7 = row.insertCell(6);
  cell1.innerHTML = (studentDict).stuName + " " + "(" + (studentDict).stuBNumber+ ")";
  cell2.innerHTML = (studentDict).stuPosition;
  $(cell2).attr("data-posn", (studentDict).stuPositionCode);
  $(cell2).attr("data-wls", (studentDict).stuWLS);
  cell2.id="position_code";
  if (termCodeLastTwo == "11" || termCodeLastTwo == "12" || termCodeLastTwo == "00") {
    cell3.innerHTML = (studentDict).stuJobType;
    cell4.innerHTML = (studentDict).stuHours;
    cell5.innerHTML = (studentDict).stuStartDate + " - " + (studentDict).stuEndDate;
    cell6.innerHTML = notesGlyphicon;
    cell7.innerHTML = removeIcon;
  }
  else {
    console.log(selectedContractHoursName);
    cell3.innerHTML = "Secondary"
    cell4.innerHTML = selectedContractHoursName;
    cell5.innerHTML = (studentDict).stuStartDate + " - " + (studentDict).stuEndDate;
    cell6.innerHTML = notesGlyphicon;
    cell7.innerHTML = removeIcon;
  }
  refreshSelectPickers();
  var rowLength = document.getElementById("mytable").rows.length;
  if (rowLength > 1) {
    $("#reviewButton").show();
  }
}

var totalHourDict = {};
function checkTotalhoursTable() {//Checks if the student has enough hours to require an overload form
}

function checkForTotalHours() {// gets sum of the total weekly hours from the database and add it to the ones in the table.
  var student = $("#student").val();
  // console.log(student);
  var term = $("#selectedTerm").val();
  // console.log(term);
  var url = "/laborstatusform/gethours/" + term +"/" +student;
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      var totalHours = 0;
      for(i = 0; i < globalArrayOfStudents.length; i++) {
         if (globalArrayOfStudents[i].stuName == student) {
           totalHours = totalHours + globalArrayOfStudents[i].stuHours;
            }
          }
      var totalWeeklyHoursFromDatabase = response.weeklyHours["Total Weekly Hours"];
      totalHours = totalWeeklyHoursFromDatabase + totalHours;
      if (totalHours > 15){ // if hours exceed 15 pop up overload modal
        $("#OverloadModal").modal("show");
        $("#overloadModalButton").attr("data-target", "#PrimaryModal");
        $("#OverloadModal").on("hidden.bs.modal", function() {
        $("#PrimaryModal").modal("show");
        });
      }
      else{
        $("#PrimaryModal").modal("show"); // modal saying primary supervisor will be notified
      }
    }
  });
}

function reviewButtonFunctionality() { // Triggred when Review button is clicked and checks if fields are filled out.
  disableTermSupervisorDept();
  var rowLength = document.getElementById("mytable").rows.length;
  if (rowLength > 1) {
     createModalContent();
  }
}

function createModalContent() { // Populates Submit Modal with Student information from the table
  var allTableDataDict = createTabledataDictionary();
  term = $("#selectedTerm").val();
  var whichTerm = term.toString().substr(-2);
  modalList = [];
  if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
    for (var key in allTableDataDict) {
      var student = allTableDataDict[key].Student;
      var studentName = student.substring(0, student.indexOf("(B0"));
      var position = allTableDataDict[key].Position;
      var selectedContractHours = allTableDataDict[key]["Contract Hours"];
      var bigString = "<li>" + studentName + " | " + position + " | " + selectedContractHours + " hours";
      modalList.push(bigString);
    }
    $("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                            "<ul style=\"display:inline-block;text-align:left;\">" +
                                                            modalList.join("</li>")+"</ul>"+
                                                            "<br><br>The labor status form will be eligible for approval in one business day.";
    $("#SubmitModal").modal("show");
  }
  else {
    for (var key in allTableDataDict) {
      var student = allTableDataDict[key].Student;
      var studentName = student.substring(0, student.indexOf("(B0"));
      var position = allTableDataDict[key].Position;
      var jobType = allTableDataDict[key]["Job Type"];
      var hours = allTableDataDict[key]["Hours Per Week"];
      var bigString = "<li>" + studentName + " | " + position + " | " + jobType + " | " + hours + " hours";
      modalList.push(bigString);
    }
    document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                            "<ul style=\"display: inline-block;text-align:left;\">" +
                                                            modalList.join("</li>")+"</ul>"+
                                                            "<br><br>The labor status form will be eligible for approval in one business day.";
    $("#SubmitModal").modal("show");
  }
}

// function createTabledataDictionary() { // puts all of the forms into dictionaries
//   var listDictAJAX = [];
//   $("#mytable tr").has("td").each(function() {
//     /* Get the input box values first */
//       var supervisor = $("#selectedSupervisor").val();
//       var department = $("#selectedDepartment").val();
//       var term = $("#selectedTerm").val();
//       var whichTerm = term.toString().substr(-2);
//       var positionCode = $("#position_code").attr("data-posn");
//       var wls = $("#position_code").attr("data-wls");
//       listDict = [];
//       listDict.push(supervisor, department, term, positionCode, wls);
//       var headersLabel = ["Supervisor", "Department", "Term", "Position Code", "WLS"];
//       var tableDataDict = {};
//       for (var i in listDict) {
//         tableDataDict[headersLabel[i]] = listDict[i];
//       }
//       /* If it"s a break, get table values */
//       if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00) {
//         tableDataDict["Job Type"] = "Secondary";
//         var headers_2_data = ["Student", "Position", "Contract Hours", "Contract Dates"];
//         $("td", $(this)).each(function(index, item) {
//           var aTag = $.parseHTML($(item).html());
//           if (!$(aTag).hasClass("remove")) {
//             var notes = $(aTag).data("note");
//             tableDataDict["Supervisor Notes"] = notes;
//             tableDataDict[headers_2_data[index]] = $(item).html();
//           }
//         });
//         listDictAJAX.push(tableDataDict);
//         allTableDataDict = {};
//         for (var key in listDictAJAX){
//           allTableDataDict[key] = listDictAJAX[key];
//         }
//       }
//       /* If it"s academic year, get the table values */
//       else {
//           var headersData = ["Student", "Position", "Job Type", "Hours Per Week", "Contract Dates"];
//           $("td", $(this)).each(function(index, item) {
//             var aTag = $.parseHTML($(item).html());
//             if (!$(aTag).hasClass("remove")) {
//               var notes = $(aTag).data("note");
//               tableDataDict["Supervisor Notes"] = notes;
//               tableDataDict[headersData[index]] = $(item).html();
//             }
//           });
//           listDictAJAX.push(tableDataDict);
//           allTableDataDict = {}; // this is the dictionary that contains all the forms
//           for (var key in listDictAJAX){
//             allTableDataDict[key] = listDictAJAX[key];
//           }
//       }
//      });
//   return allTableDataDict;
// }

// SEND DATA TO THE DATABASE
function userInsert(){
  var allTableDataDict = globalArrayOfStudents;//createTabledataDictionary();
  data = JSON.stringify(allTableDataDict);
  //alert(data)
  $("#laborStatusForm").on("submit", function(e) {
    e.preventDefault();
  });
  $.ajax({
         method: "POST",
         url: "/laborstatusform/userInsert",
         data: data,
         contentType: "application/json",
         success: function(response) {
           term = $("#selectedTerm").val();
           var whichTerm = term.toString().substr(-2);
           modalList = [];
           if (response){
             for (var key in allTableDataDict) {
               var student = allTableDataDict[key].Student;
               var studentName= student.substring(0, student.indexOf("(B0"));
               var position = allTableDataDict[key].Position;
               var selectedContractHours = allTableDataDict[key]["Contract Hours"];
               var jobType = allTableDataDict[key]["Job Type"];
               var hours = allTableDataDict[key]["Hours Per Week"];
               if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
                 var bigString = "<li>" +"<span class=\"glyphicon glyphicon-ok\" style=\"color:green\"></span> " + studentName + " | " + position + " | " + selectedContractHours + " hours";
               }
               else {
                 var bigString = "<li>"+"<span class=\"glyphicon glyphicon-ok\" style=\"color:green\"></span> " + studentName + " | " + position + " | " + jobType + " | " + hours + " hours";
              }
              modalList.push(bigString);
            }
          }
          else {
            for (var key in allTableDataDict) {

              var student = allTableDataDict[key].Student;
              var studentName = student.substring(0, student.indexOf("(B0"));
              var position = allTableDataDict[key].Position;
              var selectedContractHours = allTableDataDict[key]["Contract Hours"];
              var hours = allTableDataDict[key]["Hours Per Week"];
              if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
                var bigString = "<li>" +"<span class=\"glyphicon glyphicon-remove\" style=\"color:red\"></span> " + studentName + " | " + position + " | " + selectedContractHours + " hours";
              }
              else {
                var bigString = "<li>"+"<span class=\"glyphicon glyphicon-remove\" style=\"color:red\"></span> " + studentName + " | " + position + " | " + jobType + " | " + hours + " hours";
              }
              modalList.push(bigString);
            }
           }
         document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                                 "<ul style=\"list-style-type:none; display: inline-block;text-align:left;\">" +
                                                                 modalList.join("</li>")+"</ul>"+
                                                                 "<br><br>The labor status form will be eligible for approval in one business day.";
         $("#SubmitModal").modal("show");
       }
     });
     $("#SubmitModal").modal({backdrop: true, keyboard: false, show: true});
     $("#SubmitModal").data("bs.modal").options.backdrop = "static";
     document.getElementById("submitmodalid").innerHTML = "Done";
     document.getElementById("submitmodalid").onclick = function() { window.location.replace("/laborstatusform");};
   }
