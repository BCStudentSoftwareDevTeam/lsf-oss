$(document).ready(function(){
    $('[data-tooltip="true"]').tooltip();
});

var j = jQuery.noConflict();
j( function() {
   j( "#datetimepicker1, #datetimepicker2" ).datepicker();
} );

$(document).on('keyup', 'input[name=contracthours]', function () { // sets contract hours minimum value
   var _this = $(this);
   var min = parseInt(_this.attr('min')) || 1; // if min attribute is not defined, 1 is default
   var val = parseInt(_this.val()) || (min - 1); // if input char is not a number the value will be (min - 1) so first condition will be true
   if(val < min)
       _this.val( min );
});

// Pops up a modal for Seconday Postion
$('#jobType').change(function(){
  //this is just getting the value that is selected
  var jobType = $(this).val();
  if (jobType == "Secondary") {
      $('#SecondaryModal').modal('show');
  }
});

// Pops up a modal for overload
$('#hoursPerWeek').change(function(){
  //this is just getting the value that is selected
  var hour = $(this).val();
  if (hour == "20") {
      $('#OverloadModal').modal('show');
    }
});

function disableTerm() {
  // disables term select picker when student is selected
  $("#term").prop("disabled", "disabled");
}

function preFilledDate(obj){ // get term start date and end date
  var termCode = obj.value
  $.ajax({
    url: "/laborstatusform/getDate/" + termCode,
    dataType: "json",
    success: function (response){
       fillDates(response)
    }
  })
}

function fillDates(response){ // prefill term start and term end
  for (var key in response){
    $("#datetimepicker1").val(response[key]["Start Date"]);
    $("#datetimepicker2").val(response[key]["End Date"]);
  }
}

function getDepartment(object) { // get department from select picker
   var department = object.value;
   var url = "/laborstatusform/getPositions/" + department;
       $.ajax({
         url: url,
         dataType: "json",
         success: function (response){
            fillPositions(response)
         }
       })
 }

 function fillPositions(response) { // prefill Position select picker with the positions of the selected department
   var selectedPositions = document.getElementById("position");
   if (selectedPositions){
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


 function fillHoursPerWeek(){ // prefill hours per week select picker
  var selectedHoursPerWeek = document.getElementById("hoursPerWeek");
  var jobType = $("#jobType").val();
  if (selectedHoursPerWeek){
    $("#hoursPerWeek").empty();
    if (jobType == "Primary"){
      var options = document.createElement("option");
      var dict = {
        10: "10",
        15: "15",
        20: "20"}
      for (var key in dict){
        selectedHoursPerWeek.options[selectedHoursPerWeek.options.length]=
        new Option(dict[key], key);
      }
    }
    else if (jobType == "Secondary") {
      var options = document.createElement("option");
      var dict = {
        5: "5",
        10: "10"}
      for (var key in dict){
        selectedHoursPerWeek.options[selectedHoursPerWeek.options.length]=
        new Option(dict[key], key);
      }
    }
    $('.selectpicker').selectpicker('refresh');
  }
}

// Check if department is in compliance.
function checkCompliance(obj) {
  var department = obj.value;
  var url = "/laborstatusform/getcompliance/" + department;
      $.ajax({
        url: url,
        dataType: "json",
        success: function (response){
          if(response['Department']['Department Compliance'] == false){
            $('#OutofComplianceModal').modal('show');
            $('#term').attr('disabled', true);
            $('#datetimepicker1').attr('disabled', true);
            $('#datetimepicker2').attr('disabled', true);
            $('#student').attr('disabled', true);
            $('#position').attr('disabled', true);
            $('#jobType').attr('disabled', true);
            $('#hoursPerWeek').attr('disabled', true);
            $('#contracthours').attr('disabled', true);
          }
          else{
            $('#term').attr('disabled', false);
            $('#datetimepicker1').attr('disabled', false);
            $('#datetimepicker2').attr('disabled', false);
            $('#student').attr('disabled', false);
            $('#position').attr('disabled', false);
            $('#jobType').attr('disabled', false);
            $('#hoursPerWeek').attr('disabled', false);
            $('#contracthours').attr('disabled', false);
          }
        }
      });
}



// TABLE LABELS
$("#ContractHours").hide();
$("#Hours_PerWeek").hide();
$("#JopTypes").hide();
$("#Student").hide();
$("#Position").hide();
$("#plus").hide();
$("#mytable").hide();

function showAccessLevel(obj){ // Make Table labels appear
  $("#ContractHours").hide();
  $("#Hours_PerWeek").hide();
  $("#JopTypes").hide();
  $("#Student").hide();
  $("#Position").hide();
  $("#plus").hide();
  var termCode = obj.value;
  var whichTerm = termCode.toString().substr(-2);
  if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00) { // Summer term or any other break period table labels
    $("#Student").show();
    $("#Position").show();
    $("#ContractHours").show();
    $("#plus").show();
  }
  else{ // normal semester like Fall or Spring table labels
    $("#Student").show();
    $("#Position").show();
    $("#Hours_PerWeek").show();
    $("#JopTypes").show();
    $("#plus").show();
  }
}
// TABLE LABELS

// Table glyphicons
function showNotesModal(obj){// pops up Note Modal when notes glyphicon is clicked
  document.getElementById("modal_text").value=document.getElementById(obj).getAttribute("data-note");
  document.getElementById("saveButton").setAttribute('onclick',"saveNotes('" + obj +"')");
  $("#noteModal").modal("show");
}

function saveNotes(obj){ // saves notes written in textarea when save button of modal is clicked
  var notes = document.getElementById("modal_text").value;
  document.getElementById(obj).setAttribute("data-note", notes);
}

function deleteRow(row) { // Deletes Row when remove glyphicon is clicked.
  var i = row.parentNode.parentNode.rowIndex;
  document.getElementById('mytable').deleteRow(i);
}
//END of glyphicons

// TABLE
function displayTable(test = "") { // displays table when plus glyphicon is clicked
  $("#mytable").show();
  var termCode = $('#term').val();
  var whichTerm = termCode.toString().substr(-2);
  if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00) {
    checkDuplicateBreaks(test);
  }
  else {
    checkDuplicate(test);
  }
}

function checkDuplicate(test = "") {// checks for duplicates in the table. This is for Academic Year
    var table = document.getElementById("mytable");
    var student = document.getElementById("student");
    var studentName = student.options[student.selectedIndex].text;
    var position = document.getElementById("position");
    var positionName = position.options[position.selectedIndex].text;
    var jobType = document.getElementById("jobType");
    var jobTypeName = jobType.options[jobType.selectedIndex].text;
    var hoursPerWeek = document.getElementById("hoursPerWeek");
    var hoursPerWeekName = hoursPerWeek.options[hourPerWeek.selectedIndex].text;

    for(const tr of table.querySelectorAll("thead tr")) {
       const td0 = tr.querySelector("td:nth-child(1)");
       const td1 = tr.querySelector("td:nth-child(2)");
       const td2 = tr.querySelector("td:nth-child(3)");
       const td3 = tr.querySelector("td:nth-child(4)");
       const td4 = tr.querySelector("td:nth-child(5)");

       if(!td0 || !td1 || !td2 || !td3 || !td4) { //If we are missing cells skip it
       continue }

       if ((td0.innerHTML == studentName) && (jobTypeName == "Primary") &&(td2.innerHTML == "Primary")) {
         document.getElementById("warningModalText").innerHTML = "Match found for " +studentName +" and Primary."
         $("#warningModal").modal('show')
         $("#job_table").show();
         $("#hours_table").show();
          return;
          }

       if ((td0.innerHTML == studentName) && (td2.innerHTML == "Secondary") && (td1.innerHTML == positionName) && (jobTypeName == "Secondary")) {
         document.getElementById("warningModalText").innerHTML = "Match found for " +studentName +", "+ positionName + " and Secondary."
         $("#warningModal").modal('show')
         $("#job_table").show();
         $("#hours_table").show();
          return;
         }
  }
    checkForPrimaryPosition(test);
}

function checkForPrimaryPosition(test = ""){ // does several stuff read the comments down below
  var jobType = document.getElementById("jobType");
  var jobTypeName = jobType.options[jobType.selectedIndex].text;
  var student = $("#student").val();
  var term = $("#term").val();
  var url = "/laborstatusform/getstudents/" + term +"/" +student;
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      /* 1. Language for Primary Modal that shows up when student has a primary position and a secondary position is being submitted */
      console.log(response);
      try {
        var primarySupervisor = response["PrimarySupervisor"]["Primary Supervisor FirstName"] + " " + response["PrimarySupervisor"]["Primary Supervisor LastName"]
        document.getElementById("PrimaryModalText").innerHTML = "Secondary position has been added. Upon submission of the form, student's primary superviosr " + primarySupervisor + " will be notified."
        document.getElementById("OverloadModalText").innerHTML = "A labor overload is defined as more than 15 hours of labor per week during regular "+
                                                                "academic year and may not be approved retroactively. All approvals are subject to periodic review.<br><br>"+
                                                                "Guidlines for Approval:<br>" +
                                                                "<li>Sophomore, junior, or senior classification</li>"+
                                                                "<li>Not on any form of probation</li>"+
                                                                "<li>Enrolled in less than 5 course credits with less than 8 preparations</li>"+
                                                                "<li>Have a 2.50 GPA, both cumulative and for the previous full term</li>"+
                                                                "<li>The required 2.50 cumulative GPA may be waived if a 3.00 GPA is earned during the previous full term.</li><br>"+
                                                                "Students shoud not work any hours within a secondary assignment until notification of approved Labor Overload.\n"

      } catch (e) {
        if(jobTypeName == "Primary"){
          createAndFillTable(test);
        }
      }
      $("#job_table").show();
      $("#hours_table").show();


      /* 2. if student does not have a primary position show modal */
      var result = $.isEmptyObject(response);
      if (jobTypeName == "Secondary" && result) {
        $('#NoPrimaryModal').modal('show');
      }
      else if (jobTypeName == "Primary" && !result) { // 3. If a student already has a primary position, do not add to the table.
        document.getElementById("warningModalText").innerHTML = "Student already has a primary position."
        $("#warningModal").modal('show')
      }
      else {
      /* 4. If student has a primary position check the total hours for overload and add to table  */
          checkTotalhoursTable();
          checkForTotalHoursDatabase(test);
          createAndFillTable();
      }
    }
  });
}

function createAndFillTable() { // fills the table for Academic Year.
  var table = document.getElementById("mytable");
  var student = document.getElementById("student");
  var studentName = student.options[student.selectedIndex].text;
  var position = document.getElementById("position");
  var positionName = position.options[position.selectedIndex].text;
  var positionCode = $("#position").val()
  var jobType = document.getElementById("jobType");
  var jobTypeName = jobType.options[jobType.selectedIndex].text;
  var hoursPerWeek = document.getElementById("hoursPerWeek");
  var hoursPerWeekName = hoursPerWeek.options[hoursPerWeek.selectedIndex].text;
  var notesGlyphicon = "<a data-toggle='modal' onclick = 'showNotesModal(\""+String(studentName) + String(jobTypeName) + String(positionName)+"\")' id= '"+String(studentName) +
                                                          String(jobTypeName) + String(positionName)+"' ><span class='glyphicon glyphicon-edit'></span></a>";
  var removeIcon = "<a onclick = 'deleteRow(this)' class='remove'><span class='glyphicon glyphicon-remove'></span></a>";

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
  var cell5 = row.insertCell(4);
  var cell6 = row.insertCell(5);

  cell1.innerHTML = studentName;
  cell2.innerHTML = positionName;
  $(cell2).attr("data-posn", positionCode);
  cell2.id="position_code";
  cell3.innerHTML = jobTypeName;
  cell4.innerHTML = hoursPerWeekName;
  cell5.innerHTML = notesGlyphicon;
  cell6.innerHTML = removeIcon;


  $("#hoursPerWeek").val('default');
  $("#hoursPerWeek").selectpicker("refresh");
  $("#jobType").val('default');
  $("#jobType").selectpicker("refresh");
  $("#student").val('default');
  $("#student").selectpicker("refresh");
  $("#position").val('default');
  $("#position").selectpicker("refresh");

}


var totalHourDict = {}
function checkTotalhoursTable() {//Checks if the student has enough hours to require an overload form
  var table = document.getElementById("mytable");
  var student = document.getElementById("student");
  var studentName = student.options[student.selectedIndex].text;
  var totalHours = 0
  var hoursPerWeek = document.getElementById("hoursPerWeek");
  var hoursPerWeekName = hoursPerWeek.options[hoursPerWeek.selectedIndex].text;
  for(const tr of table.querySelectorAll("thead tr")) {
     const td0 = tr.querySelector("td:nth-child(1)");
     const td2 = tr.querySelector("td:nth-child(4)");
     if ((td0.innerHTML == studentName)) {
       totalHours = totalHours + parseInt(td2.innerHTML);
        }
      }
  totalHours = totalHours + parseInt(hoursPerWeekName);
  totalHourDict["total"] = {totalHours}
}


function checkForTotalHoursDatabase(test = "") {// gets sum of the total weekly hours from the database and add it to the ones in the table.
  var student = $("#student").val();
  var term = $("#term").val();
  var url = "/laborstatusform/gethours/" + term +"/" +student;
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      var totalWeeklyHoursFromDatabase = response["weeklyHours"]["Total Weekly Hours"]
      var totalWeeklyHoursFromTable = totalHourDict["total"]["totalHours"]
      var total = totalWeeklyHoursFromDatabase + totalWeeklyHoursFromTable
      if (total > 15){ // if hours exceed 15 pop up overload modal
        $('#OverloadModal').modal('show');
        $('#OverloadModal').on('hidden.bs.modal', function() {
          $('#PrimaryModal').on('hidden.bs.modal', function() {
          if (test == 'test') {
            createModalContent()
            }
          });
        });
      }
      else{
        $('#PrimaryModal').modal('show'); // modal saying primary superviosr will be notified
        $('#PrimaryModal').on('hidden.bs.modal', function() {
          if (test == 'test') {
            createModalContent()
          }
        });
      }
    }
  });
}


// THIS IS FOR BREAKSSSS
function checkDuplicateBreaks(test = "") { // checks for duplicates in table. For summer or any other break.
      var table = document.getElementById("mytable");
      var student = document.getElementById("student");
      var studentName = student.options[student.selectedIndex].text;
      var position = document.getElementById("position");
      var positionName = position.options[position.selectedIndex].text;

      for(const tr of table.querySelectorAll("thead tr")) {
         const td0 = tr.querySelector("td:nth-child(1)");
         const td1 = tr.querySelector("td:nth-child(2)");
         const td2 = tr.querySelector("td:nth-child(3)");

         if ((td0.innerHTML == studentName) && (td1.innerHTML==positionName)) {
           document.getElementById("warningModalText").innerHTML = "Match found for " +studentName +" and " + positionName
           $("#warningModal").modal('show')
            $("#contract_table").show();
            return;
            }
          }
          createAndFillTableForBreaks(test)
        }

function createAndFillTableForBreaks(test = '') {// Fills the table. For Summer term or any other break period
  $("#mytable").show();
  $("#job_table").hide();
  $("#hours_table").hide();
  $("#primary_table").hide();
  $("#contract_table").show();
  var table = document.getElementById("mytable");
  var student = document.getElementById("student");
  var studentName = student.options[student.selectedIndex].text;
  var position = document.getElementById("position");
  var positionName = position.options[position.selectedIndex].text;
  var positionCode = $("#position").val()
  var contractHoursName = document.getElementById("contracthours").value;
  var notesGlyphicon = "<a data-toggle='modal' onclick = 'showNotesModal(\""+String(studentName) + String(positionName)+"\")' id= '"+String(studentName) +
                                                          String(positionName)+"' ><span class='glyphicon glyphicon-edit'></span></a>";
  var removeIcon = "<a onclick = 'deleteRow(this)' class='remove'><span class='glyphicon glyphicon-remove'></span></a>";


  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  $(cell2).attr("data-posn", positionCode);
  cell2.id="position_code";
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);
  var cell5 = row.insertCell(4);

  cell1.innerHTML = studentName;
  cell2.innerHTML = positionName;
  cell3.innerHTML = contractHoursName;
  cell4.innerHTML = notesGlyphicon;
  cell5.innerHTML = removeIcon;

  $("#contracthours").val('');
  $("#position").val('default');
  $("#position").selectpicker("refresh");
  $("#student").val('default');
  $("#student").selectpicker("refresh");

  if (test == 'test'){
    createModalContent()
  }
}
// END OF (THIS IS FOR BREAKSSSS)


function reviewButtonFunctionality(test) { // Triggred when Review button is clicked
  if( !$('#student').val() ) {
    var rowLength = document.getElementById("mytable").rows.length;
    if (rowLength > 1) {
       createModalContent();
    }
  }
  else{
    displayTable(test); // the passed argument is used to prevent plus glyphicon from submitting the form.
  }
}

function createModalContent() { // Populates Submit Modal with Student information from the table
  var testDict = createTabledataDictionary();
  term = $("#term").val();
  var whichTerm = term.toString().substr(-2);
  modalList = [];

  if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
    for (var key in testDict) {
      var student = testDict[key]["Student"];
      var position = testDict[key]["Position"];
      var contractHours = testDict[key]["Contract Hours"];
      var bigString = "<li>" + student + ' | ' + position + ' | ' + contractHours;
      modalList.push(bigString)
    }
    document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                            "<ul style='display: inline-block;text-align:left;'>" +
                                                            modalList.join("</li>")+"</ul>"+
                                                            "<br><br>The labor status form will be eligible for approval in one business day."
    $('#SubmitModal').modal('show')
  }
  else {
    for (var key in testDict) {
      var student = testDict[key]["Student"];
      var position = testDict[key]["Position"];
      var jobType = testDict[key]["Job Type"];
      var hours = testDict[key]["Hours Per Week"];
      var bigString = "<li>" + student + ' | ' + position + ' | ' + jobType + ' | ' + hours;
      modalList.push(bigString)
    }
    document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                            "<ul style='display: inline-block;text-align:left;'>" +
                                                            modalList.join("</li>")+"</ul>"+
                                                            "<br><br>The labor status form will be eligible for approval in one business day."
    $('#SubmitModal').modal('show')
  }
}


function createTabledataDictionary() { // puts all of the forms into dictionaries
  var listDictAJAX = [];
  $('#mytable tr').has('td').each(function() {
    /* Get the input box values first */
      supervisor = $("#supervisor").val();
      department = $("#department").val();
      term = $("#term").val();
      var whichTerm = term.toString().substr(-2);
      startDate = $("#datetimepicker1").val();
      endDate = $("#datetimepicker2").val();
      var positionCode = $("#position_code").attr("data-posn");
      listDict = []
      listDict.push(supervisor, department, term, startDate, endDate, positionCode)
      var headersLabel = ["Supervisor", "Department", "Term", "Start Date", "End Date", "Position Code"]
      var tableDataDict = {};
      for (i in listDict) {
        tableDataDict[headersLabel[i]] = listDict[i];
      }

      /* If it's a break, get table values */
      if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00) {
        tableDataDict["Job Type"] = "Secondary";
        var headers_2_data = ["Student", "Position", "Contract Hours"];
        $('td', $(this)).each(function(index, item) {
          var aTag = $.parseHTML($(item).html());
          if (!$(aTag).hasClass('remove')) {
            var notes = $(aTag).data('note');
            tableDataDict["Supervisor Notes"] = notes;
            tableDataDict[headers_2_data[index]] = $(item).html();
          }
        });
        listDictAJAX.push(tableDataDict);
        testDict = {}
        for ( var key in listDictAJAX){
          testDict[key] = listDictAJAX[key];
        }
      }
      /* If it's academic year, get the table values */
      else {
          var headersData = ["Student", "Position", "Job Type", "Hours Per Week"];
          $('td', $(this)).each(function(index, item) {
            var aTag = $.parseHTML($(item).html());
            if (!$(aTag).hasClass('remove')) {
              var notes = $(aTag).data('note');
              tableDataDict["Supervisor Notes"] = notes;
              tableDataDict[headersData[index]] = $(item).html();
            }
          });
          listDictAJAX.push(tableDataDict);
          testDict = {} // FIXME rename to something else, this is the dictionary that contains all the forms
          for ( var key in listDictAJAX){
            testDict[key] = listDictAJAX[key];
          }
      }
     });

  delete testDict["0"] // gets rid of the first dictionary that contains table labels
  return testDict
}

// SEND DATA TO THE DATABASE
function userInsert(){
  var testDict = createTabledataDictionary()
  data = JSON.stringify(testDict);
  $('#laborStatusForm').on('submit', function(e) {
    e.preventDefault();
  });
  $.ajax({
         method: "POST",
         url: '/laborstatusform/userInsert',
         data: data,
         contentType: 'application/json',
         success: function(response) {
           term = $("#term").val();
           var whichTerm = term.toString().substr(-2);
           modalList = [];
           if (response){
             for (var key in testDict) {
               var student = testDict[key]["Student"];
               var position = testDict[key]["Position"];
               var contractHours = testDict[key]["Contract Hours"];
               var jobType = testDict[key]["Job Type"];
               var hours = testDict[key]["Hours Per Week"];
               if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
                 var bigString = "<li>" +"<span class='glyphicon glyphicon-ok' style='color:green'></span> " + student + ' | ' + position + ' | ' + contractHours;
               }
               else {
                 var bigString = "<li>"+"<span class='glyphicon glyphicon-ok' style='color:green'></span> " + student + ' | ' + position + ' | ' + jobType + ' | ' + hours;
              }
              modalList.push(bigString)
            }
          }

          else {
            for (var key in testDict) {
               var student = testDict[key]["Student"];
               var position = testDict[key]["Position"];
               var contractHours = testDict[key]["Contract Hours"];
               var hours = testDict[key]["Hours Per Week"];

              if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
               var bigString = "<li>" +"<span class='glyphicon glyphicon-remove' style='color:red'></span> " + student + ' | ' + position + ' | ' + contractHours;
              }
              else {
                var bigString = "<li>"+"<span class='glyphicon glyphicon-remove' style='color:red'></span> " + student + ' | ' + position + ' | ' + jobType + ' | ' + hours;
              }
              modalList.push(bigString)
            }
           }
         document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                                 "<ul style='display: inline-block;text-align:left;'>" +
                                                                 modalList.join("</li>")+"</ul>"+
                                                                 "<br><br>The labor status form will be eligible for approval in one business day."
         $('#SubmitModal').modal('show')
       }
     });

     $('#SubmitModal').modal({backdrop: true, keyboard: false, show: true});
     $('#SubmitModal').data('bs.modal').options.backdrop = 'static';
     document.getElementById('submitmodalid').innerHTML = "Done";
     document.getElementById('submitmodalid').onclick = function() { window.location.reload();}
}
