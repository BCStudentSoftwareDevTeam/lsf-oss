$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip()
});


$( "laborStatusForm" ).submit(function( event ) {
  alert( "Handler for .submit() called." );
  event.preventDefault();
});

$(document).ready(function(){
    $('[data-tooltip="true"]').tooltip();
    $( "#dateTimePicker1, #dateTimePicker2" ).datepicker();
});

$(document).on('keyup', 'input[name=contractHours]', function () { // sets contract hours minimum value
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
$('#selectedHoursPerWeek').change(function(){
  //this is just getting the value that is selected
  var hour = $(this).val();
  if (hour == "20") {
      $('#OverloadModal').modal('show');
      $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
    }
});

function disableTerm() {
  // disables term select picker when student is selected
  $("#selectedTerm").prop("disabled", "disabled");
  $("#termInfo").show();
  $('#selectedTerm').selectpicker('refresh');
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
    var start = response[key]['Start Date'];
    var end = response[key]["End Date"];
    // Start Date
    var startd = new Date(start)
    var dayStart = startd.getDate();
    var monthStart = startd.getMonth();
    var yearStart = startd.getFullYear();
    // End Date
    var endd = new Date(end)
    var dayEnd = endd.getDate();
    var monthEnd = endd.getMonth();
    var yearEnd = endd.getFullYear();
    // Pre-populate values
    $("#dateTimePicker1").val(start);
    $("#dateTimePicker2").val(end);
    // set the minimum and maximum Date for Term Start Date
    $('#dateTimePicker1').datepicker({minDate: new Date(yearStart, monthStart, dayStart)});
    $('#dateTimePicker1').datepicker({maxDate: new Date(yearEnd, monthEnd, dayEnd)});
    $( "#dateTimePicker1" ).datepicker( "option", "minDate", new Date(yearStart, monthStart, dayStart) );
    $( "#dateTimePicker1" ).datepicker( "option", "maxDate", new Date(yearEnd, monthEnd, dayEnd));
    // set the minimum and maximum Date for Term End Date
    $('#dateTimePicker2').datepicker({maxDate: new Date(yearEnd, monthEnd, dayEnd)});
    $('#dateTimePicker2').datepicker({minDate: new Date(yearStart, monthStart, dayStart)});
    $( "#dateTimePicker2" ).datepicker( "option", "maxDate", new Date(yearEnd, monthEnd, dayEnd));
    $( "#dateTimePicker2" ).datepicker( "option", "minDate", new Date(yearStart, monthStart, dayStart) );
  }
}

function updateStart(obj){ // updates the max date of the start datepicker to not be after what the end datePicker picked
  var newEnd = new Date(obj.value)
  var dayNewEnd = newEnd.getDate() - 1;
  var monthNewEnd = newEnd.getMonth();
  var yearNewEnd = newEnd.getFullYear();
  $('#dateTimePicker1').datepicker({maxDate: new Date(yearNewEnd, monthNewEnd, dayNewEnd)});
  $( "#dateTimePicker1" ).datepicker( "option", "maxDate", new Date(yearNewEnd, monthNewEnd, dayNewEnd));
}

function updateEnd(obj){ // updates the max date of the end datepicker to not be before what the start datePicker picked
  var newStart = new Date(obj.value)
  var dayNewStart = newStart.getDate() + 1;
  var monthNewStart = newStart.getMonth();
  var yearNewStart = newStart.getFullYear();
  $('#dateTimePicker2').datepicker({minDate: new Date(yearNewStart, monthNewStart, dayNewStart)});
  $( "#dateTimePicker2" ).datepicker( "option", "minDate", new Date(yearNewStart, monthNewStart, dayNewStart));
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
       options.text = response[key]["position"].toString() + " " + "(" + response[key]["WLS"].toString() + ")";
       options.id = key;
       options.value = response[key]['WLS'];
       selectedPositions.appendChild(options);
     }
       $('.selectpicker').selectpicker('refresh');
   }
 }

 // Pops up a modal for WLS 5, 6 or more
 $('#position').change(function(){
   //this is just getting the value that is selected
   var wls = $('#position').find('option:selected').attr('value');
   if (wls >= 5) {
     document.getElementById('WLSModalTitle').innerHTML = "Work-Learning-Service Levels (WLS)"
     document.getElementById('WLSModalText').innerHTML = "Student with WLS Level 5 or 6 must have at least a 15 hour contract. " +
                                                        "These positions require special authorization as specified at " +
                                                        "<a href='http://catalog.berea.edu/2014-2015/Tools/Work-Learning-Service-Levels-WLS' target='_blank'>The Labor Program Website.</a>";
     $('#WLSModal').modal('show');
     }
 });


 function fillHoursPerWeek(fillhours=""){ // prefill hours per week select picker
  var selectedHoursPerWeek = document.getElementById("selectedHoursPerWeek");
  var jobType = $("#jobType").val();
  if (selectedHoursPerWeek){
    $("#selectedHoursPerWeek").empty();
    if (jobType == "Primary"){
      var options = document.createElement("option");
      var dict = {
        10: "10",
        15: "15",
        20: "20"}
      for (var key in dict){
        selectedHoursPerWeek.options[selectedHoursPerWeek.options.length]= new Option(dict[key], key);
      }
    }
    else if (jobType == "Secondary") {
      var options = document.createElement("option");
      var dict = {
        5: "5",
        10: "10"}
      for (var key in dict){
        selectedHoursPerWeek.options[selectedHoursPerWeek.options.length]= new Option(dict[key], key);
      }
    }
    if (fillhours == ""){
      $('.selectpicker').selectpicker('refresh');
    }
  }
}

if(document.getElementById('jobType').value){// fills hours per week selectpicker with correct information from laborstatusform. This is triggered on redirect from form history.
  var value = $('#selectedHoursPerWeek').val();
  $('#selectedHoursPerWeek').val(value);
  fillHoursPerWeek("fillhours");
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
            $('.disable').prop('disabled', true);
          }
          else{
            $('.disable').prop('disabled', false);
          }
        }
      });
}

//refresh select pickers
function refreshSelectPickers() {
  $("#selectedContractHours").val('');
  $("#selectedHoursPerWeek").val('default');
  $("#selectedHoursPerWeek").selectpicker("refresh");
  $("#jobType").val('default');
  $("#jobType").selectpicker("refresh");
  $("#student").val('default');
  $("#student").selectpicker("refresh");
  $("#position").val('default');
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
  var termCode = obj.value;
  var whichTerm = termCode.toString().substr(-2);
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
$('#reviewButton').hide()
//end

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
function displayTable() { // displays table when plus glyphicon is clicked and check if fields are filled out
  if ($('#selectedSupervisor').val()=="" || $('#selectedDepartment').val()=="" || $('#selectedTerm').val()=="" || $("#dateTimePicker1").val()=="" || $("#dateTimePicker2").val()=="") {
    category = "danger"
    msg = "Please fill out all fields before submitting.";
    $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
    $("#flasher").delay(3000).fadeOut()

  }
  else {
    var termCode = $('#selectedTerm').val();
    var whichTerm = termCode.toString().substr(-2);
    if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00) {
      if ($('#student').val()=="" || $('#student').val()==null || $('#position').val()=="" || $('#position').val()==null || $('#selectedContractHours').val()=="") {
        category = "danger"
        msg = "Please fill out all fields before submitting.";
        $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
        $("#flasher").delay(3000).fadeOut()
      }
      else {
        checkDuplicateBreaks();
       }
      }
    else {
      if ($('#student').val()=="" || $('#student').val()==null || $('#position').val()=="" || $('#position').val()==null || $('#jobType').val()=="" || $('#jobType').val()==null || $('#selectedHoursPerWeek').val()=="" || $('#selectedHoursPerWeek').val()==null) {
        category = "danger"
        msg = "Please fill out all fields before submitting.";
        $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
        $("#flasher").delay(3000).fadeOut()
      }
      else {
        checkDuplicate();
      }
    }
  }
}

function checkDuplicate() {// checks for duplicates in the table. This is for Academic Year
    var table = document.getElementById("mytable").getElementsByTagName('tbody')[0];
    var student = document.getElementById("student");
    var studentName = student.options[student.selectedIndex].text;
    var position = document.getElementById("position");
    var positionName = position.options[position.selectedIndex].text;
    var jobType = document.getElementById("jobType");
    var jobTypeName = jobType.options[jobType.selectedIndex].text;
    var hoursPerWeek = document.getElementById("selectedHoursPerWeek");
    var hoursPerWeekName = hoursPerWeek.options[hoursPerWeek.selectedIndex].text;

    for(const tr of table.querySelectorAll("tbody tr")) {
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
         $("#jobTable").show();
         $("#hoursTable").show();
         refreshSelectPickers()
          return;
          }

       if ((td0.innerHTML == studentName) && (td2.innerHTML == "Secondary") && (td1.innerHTML == positionName) && (jobTypeName == "Secondary")) {
         document.getElementById("warningModalText").innerHTML = "Match found for " +studentName +", "+ positionName + " and Secondary."
         $("#warningModal").modal('show')
         $("#jobTable").show();
         $("#hoursTable").show();
         refreshSelectPickers()
          return;
         }
  }
    checkForPrimaryPosition();
}

function checkForPrimaryPosition(){ // does several stuff read the comments down below
  var student = document.getElementById("student");
  var studentName = student.options[student.selectedIndex].text;
  var jobType = document.getElementById("jobType");
  var jobTypeName = jobType.options[jobType.selectedIndex].text;
  var student = $("#student").val();
  var term = $("#selectedTerm").val();
  var url = "/laborstatusform/getstudents/" + term +"/" +student;
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      /* 1. Language for Primary Modal that shows up when student has a primary position and a secondary position is being submitted */
      try {
        var primary_supervisor = response["PrimarySupervisor"]["Primary Supervisor FirstName"] + " " + response["PrimarySupervisor"]["Primary Supervisor LastName"]
        document.getElementById("PrimaryModalText").innerHTML = "Secondary position has been added. Upon submission of the form, student's primary supervisor " +
                                                                primary_supervisor + " will be notified."
      }
      catch (e) {
        if(jobTypeName == "Primary"){

          createAndFillTable();
        }
      }
      $("#jobTable").show();
      $("#hoursTable").show();


      /* 2. if student does not have a primary position show modal */
      var result = $.isEmptyObject(response);
      if (jobTypeName == "Secondary" && result) {
        document.getElementById('NoPrimaryModalText').innerHTML = "<span class='glyphicon glyphicon-exclamation-sign' style='color:red; font-size:20px;'></span>"+
                                                                  " The selected student " + studentName +" does not have a primary position."
        $('#NoPrimaryModal').modal('show');
        refreshSelectPickers();
      }
      else if (jobTypeName == "Primary" && !result) { // 3. If a student already has a primary position, do not add to the table.
        document.getElementById("warningModalText").innerHTML =  studentName + " already has a primary position."
        $("#warningModal").modal('show')
        refreshSelectPickers();
      }
      else {
      /* 4. If student has a primary position check the total hours for overload and add to table  */
          checkTotalhoursTable();
          checkForTotalHoursDatabase();
          createAndFillTable();
      }
    }
  });
}

function createAndFillTable() { // fills the table for Academic Year.
  var table = document.getElementById("mytable").getElementsByTagName('tbody')[0];
  var student = document.getElementById("student");
  var studentName = student.options[student.selectedIndex].text;
  var position = document.getElementById("position");
  var positionName = position.options[position.selectedIndex].text;
  var positionCode = $("#position").find('option:selected').attr('id');
  var jobType = document.getElementById("jobType");
  var jobTypeName = jobType.options[jobType.selectedIndex].text;
  var hoursPerWeek = document.getElementById("selectedHoursPerWeek");
  var hoursPerWeekName = hoursPerWeek.options[hoursPerWeek.selectedIndex].text;
  var notesGlyphicon = "<a data-toggle='modal' onclick = 'showNotesModal(\""+String(studentName) + String(jobTypeName) + String(positionName)+"\")' id= '"+String(studentName) +
                                                          String(jobTypeName) + String(positionName)+"' ><span class='glyphicon glyphicon-edit'></span></a>";
  var removeIcon = "<a onclick = 'deleteRow(this)' class='remove'><span class='glyphicon glyphicon-remove'></span></a>";

  $("#mytable").show();
  $("#jobTable").show();
  $("#hoursTable").show();
  $("#contractTable").hide();
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
  refreshSelectPickers();

  var rowLength = document.getElementById("mytable").rows.length;
  if (rowLength > 1) {
    $('#reviewButton').show();
  }

}


var totalHourDict = {}
function checkTotalhoursTable() {//Checks if the student has enough hours to require an overload form
  var table = document.getElementById("mytable").getElementsByTagName('tbody')[0];
  var student = document.getElementById("student");
  var studentName = student.options[student.selectedIndex].text;
  var totalHours = 0
  var hoursPerWeek = document.getElementById("selectedHoursPerWeek");
  var hoursPerWeekName = hoursPerWeek.options[hoursPerWeek.selectedIndex].text;
  for(const tr of table.querySelectorAll("tbody tr")) {
     const td0 = tr.querySelector("td:nth-child(1)");
     const td2 = tr.querySelector("td:nth-child(4)");
     if ((td0.innerHTML == studentName)) {
       totalHours = totalHours + parseInt(td2.innerHTML);
        }
      }
  totalHours = totalHours + parseInt(hoursPerWeekName);
  totalHourDict["total"] = {totalHours}
}


function checkForTotalHoursDatabase() {// gets sum of the total weekly hours from the database and add it to the ones in the table.
  var student = $("#student").val();
  var term = $("#selectedTerm").val();
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
        $('#overloadModalButton').attr('data-target', '#PrimaryModal')
        $('#OverloadModal').on('hidden.bs.modal', function() {
        $('#PrimaryModal').modal('show');
        });
      }
      else{
        $('#PrimaryModal').modal('show'); // modal saying primary supervisor will be notified
      }
    }
  });
}


// THIS IS FOR BREAKSSSS
function checkDuplicateBreaks() { // checks for duplicates in table. For summer or any other break.
    var table = document.getElementById("mytable").getElementsByTagName('tbody')[0];
    var student = document.getElementById("student");
    var studentName = student.options[student.selectedIndex].text;
    var position = document.getElementById("position");
    var positionName = position.options[position.selectedIndex].text;

    for(const tr of table.querySelectorAll("tbody tr")) {
       const td0 = tr.querySelector("td:nth-child(1)");
       const td1 = tr.querySelector("td:nth-child(2)");
       const td2 = tr.querySelector("td:nth-child(3)");

       if ((td0.innerHTML == studentName) && (td1.innerHTML==positionName)) {
         document.getElementById("warningModalText").innerHTML = "Match found for " +studentName +" and " + positionName
         $("#warningModal").modal('show')
          $("#contractTable").show();
          refreshSelectPickers();
          return;
          }
        }
        createAndFillTableForBreaks()
      }

function createAndFillTableForBreaks() {// Fills the table. For Summer term or any other break period
  $("#mytable").show();
  $("#jobTable").hide();
  $("#hoursTable").hide();
  $("#contractTable").show();
  var table = document.getElementById("mytable").getElementsByTagName('tbody')[0];
  var student = document.getElementById("student");
  var studentName = student.options[student.selectedIndex].text;
  var position = document.getElementById("position");
  var positionName = position.options[position.selectedIndex].text;
  var positionCode = $("#position").find('option:selected').attr('id');
  var selectedContractHoursName = document.getElementById("selectedContractHours").value;
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
  cell3.innerHTML = selectedContractHoursName;
  cell4.innerHTML = notesGlyphicon;
  cell5.innerHTML = removeIcon;

  refreshSelectPickers();

  var rowLength = document.getElementById("mytable").rows.length;
  if (rowLength > 1) {
    $('#reviewButton').show();
  }
}
// END OF (THIS IS FOR BREAKSSSS)


function reviewButtonFunctionality() { // Triggred when Review button is clicked and checks if fields are filled out.
  disableTerm();
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
      var student = allTableDataDict[key]["Student"];
      var studentName = student.substring(0, student.indexOf('(B0'));
      var position = allTableDataDict[key]["Position"];
      var selectedContractHours = allTableDataDict[key]["Contract Hours"];
      var bigString = "<li>" + studentName + ' | ' + position + ' | ' + selectedContractHours + ' hours';
      modalList.push(bigString)
    }
    document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                            "<ul style='display:inline-block;text-align:left;'>" +
                                                            modalList.join("</li>")+"</ul>"+
                                                            "<br><br>The labor status form will be eligible for approval in one business day."
    $('#SubmitModal').modal('show')
  }
  else {
    for (var key in allTableDataDict) {
      var student = allTableDataDict[key]["Student"];
      var studentName = student.substring(0, student.indexOf('(B0'));
      var position = allTableDataDict[key]["Position"];
      var jobType = allTableDataDict[key]["Job Type"];
      var hours = allTableDataDict[key]["Hours Per Week"];
      var bigString = "<li>" + studentName + ' | ' + position + ' | ' + jobType + ' | ' + hours + ' hours';
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
      supervisor = $("#selectedSupervisor").val();
      department = $("#selectedDepartment").val();
      term = $("#selectedTerm").val();
      var whichTerm = term.toString().substr(-2);
      startDate = $("#dateTimePicker1").val();
      endDate = $("#dateTimePicker2").val();
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
        allTableDataDict = {}
        for ( var key in listDictAJAX){
          allTableDataDict[key] = listDictAJAX[key];
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
          allTableDataDict = {} // this is the dictionary that contains all the forms
          for ( var key in listDictAJAX){
            allTableDataDict[key] = listDictAJAX[key];
          }
      }
     });
  return allTableDataDict
}

// SEND DATA TO THE DATABASE
function userInsert(){
  var allTableDataDict = createTabledataDictionary()
  data = JSON.stringify(allTableDataDict);
  $('#laborStatusForm').on('submit', function(e) {
    e.preventDefault();
  });
  $.ajax({
         method: "POST",
         url: '/laborstatusform/userInsert',
         data: data,
         contentType: 'application/json',
         success: function(response) {
           term = $("#selectedTerm").val();
           var whichTerm = term.toString().substr(-2);
           modalList = [];
           if (response){
             for (var key in allTableDataDict) {
               var student = allTableDataDict[key]["Student"];
               var studentName= student.substring(0, student.indexOf('(B0'));
               var position = allTableDataDict[key]["Position"];
               var selectedContractHours = allTableDataDict[key]["Contract Hours"];
               var jobType = allTableDataDict[key]["Job Type"];
               var hours = allTableDataDict[key]["Hours Per Week"];
               if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
                 var bigString = "<li>" +"<span class='glyphicon glyphicon-ok' style='color:green'></span> " + studentName + ' | ' + position + ' | ' + selectedContractHours + ' hours';
               }
               else {
                 var bigString = "<li>"+"<span class='glyphicon glyphicon-ok' style='color:green'></span> " + studentName + ' | ' + position + ' | ' + jobType + ' | ' + hours + ' hours';
              }
              modalList.push(bigString)
            }
          }

          else {
            for (var key in allTableDataDict) {
               var student = allTableDataDict[key]["Student"];
               var studentName = student.substring(0, student.indexOf('(B0'));
               var position = allTableDataDict[key]["Position"];
               var selectedContractHours = allTableDataDict[key]["Contract Hours"];
               var hours = allTableDataDict[key]["Hours Per Week"];

              if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
               var bigString = "<li>" +"<span class='glyphicon glyphicon-remove' style='color:red'></span> " + studentName + ' | ' + position + ' | ' + selectedContractHours + ' hours';
              }
              else {
                var bigString = "<li>"+"<span class='glyphicon glyphicon-remove' style='color:red'></span> " + studentName + ' | ' + position + ' | ' + jobType + ' | ' + hours + ' hours';
              }
              modalList.push(bigString)
            }
           }
         document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                                 "<ul style='list-style-type:none; display: inline-block;text-align:left;'>" +
                                                                 modalList.join("</li>")+"</ul>"+
                                                                 "<br><br>The labor status form will be eligible for approval in one business day."
         $('#SubmitModal').modal('show')
       }
     });

     $('#SubmitModal').modal({backdrop: true, keyboard: false, show: true});
     $('#SubmitModal').data('bs.modal').options.backdrop = 'static';
     document.getElementById('submitmodalid').innerHTML = "Done";
     document.getElementById('submitmodalid').onclick = function() { window.location.replace("/laborstatusform");}
}
