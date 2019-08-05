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
  // disables term select picker when student is selected
  $("#term").prop("disabled", "disabled");
}

function preFilledDate(obj){ // get term start date and end date
  var termcode = obj.value
  $.ajax({
    url: "/laborstatusform/getDate/" + termcode,
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


 function fillHoursPerWeek(){ // prefill hours per week select picker
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
            $('#jobtype').attr('disabled', true);
            $('#hours_perweek').attr('disabled', true);
            $('#contracthours').attr('disabled', true);
          }
          else{
            $('#term').attr('disabled', false);
            $('#datetimepicker1').attr('disabled', false);
            $('#datetimepicker2').attr('disabled', false);
            $('#student').attr('disabled', false);
            $('#position').attr('disabled', false);
            $('#jobtype').attr('disabled', false);
            $('#hours_perweek').attr('disabled', false);
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
  var termcode = obj.value;
  var whichterm = termcode.toString().substr(-2);
  if (whichterm != 11 && whichterm !=12 && whichterm !=00) { // Summer term or any other break period table labels
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
  var termcode = $('#term').val();
  var whichterm = termcode.toString().substr(-2);
  if (whichterm != 11 && whichterm !=12 && whichterm !=00) {
    checkDuplicateBreaks(test);
  }
  else {
    checkDuplicate(test);
  }
}

function checkDuplicate(test = "") {// checks for duplicates in the table. This is for Academic Year
    var table = document.getElementById("mytable");
    var student = document.getElementById("student");
    var studentname = student.options[student.selectedIndex].text;
    var position = document.getElementById("position");
    var positionname = position.options[position.selectedIndex].text;
    var jobtype = document.getElementById("jobtype");
    var jobtypename = jobtype.options[jobtype.selectedIndex].text;
    var hours_perweek = document.getElementById("hours_perweek");
    var hours_perweekname = hours_perweek.options[hours_perweek.selectedIndex].text;

    for(const tr of table.querySelectorAll("thead tr")) {
       const td0 = tr.querySelector("td:nth-child(1)");
       const td1 = tr.querySelector("td:nth-child(2)");
       const td2 = tr.querySelector("td:nth-child(3)");
       const td3 = tr.querySelector("td:nth-child(4)");
       const td4 = tr.querySelector("td:nth-child(5)");

       if(!td0 || !td1 || !td2 || !td3 || !td4) { //If we are missing cells skip it
       continue }

       if ((td0.innerHTML == studentname) && (jobtypename == "Primary") &&(td2.innerHTML == "Primary")) {
         document.getElementById("warningModalText").innerHTML = "Match found for " +studentname +" and Primary."
         $("#warningModal").modal('show')
         $("#job_table").show();
         $("#hours_table").show();
          return;
          }

       if ((td0.innerHTML == studentname) && (td2.innerHTML == "Secondary") && (td1.innerHTML == positionname) && (jobtypename == "Secondary")) {
         document.getElementById("warningModalText").innerHTML = "Match found for " +studentname +", "+ positionname + " and Secondary."
         $("#warningModal").modal('show')
         $("#job_table").show();
         $("#hours_table").show();
          return;
         }
  }
    checkForPrimaryPosition(test);
}

function checkForPrimaryPosition(test = ""){ // does several stuff read the comments down below
  var jobtype = document.getElementById("jobtype");
  var jobtypename = jobtype.options[jobtype.selectedIndex].text;
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
        var primary_supervisor = response["PrimarySupervisor"]["Primary Supervisor FirstName"] + " " + response["PrimarySupervisor"]["Primary Supervisor LastName"]
        document.getElementById("PrimaryModalText").innerHTML = "Secondary position has been added. Upon submission of the form, student's primary superviosr " + primary_supervisor + " will be notified."
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
        if(jobtypename == "Primary"){
          createAndFillTable(test);
        }
      }
      $("#job_table").show();
      $("#hours_table").show();


      /* 2. if student does not have a primary position show modal */
      var result = $.isEmptyObject(response);
      if (jobtypename == "Secondary" && result) {
        $('#NoPrimaryModal').modal('show');
      }
      else if (jobtypename == "Primary" && !result) { // 3. If a student already has a primary position, do not add to the table.
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
  var studentname = student.options[student.selectedIndex].text;
  var position = document.getElementById("position");
  var positionname = position.options[position.selectedIndex].text;
  var posn_code = $("#position").val()
  var jobtype = document.getElementById("jobtype");
  var jobtypename = jobtype.options[jobtype.selectedIndex].text;
  var hours_perweek = document.getElementById("hours_perweek");
  var hours_perweekname = hours_perweek.options[hours_perweek.selectedIndex].text;
  var notesGlyphicon = "<a data-toggle='modal' onclick = 'showNotesModal(\""+String(studentname) + String(jobtypename) + String(positionname)+"\")' id= '"+String(studentname) +
                                                          String(jobtypename) + String(positionname)+"' ><span class='glyphicon glyphicon-edit'></span></a>";
  var remove_icon = "<a onclick = 'deleteRow(this)' class='remove'><span class='glyphicon glyphicon-remove'></span></a>";

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

  cell1.innerHTML = studentname;
  cell2.innerHTML = positionname;
  $(cell2).attr("data-posn", posn_code);
  cell2.id="position_code";
  cell3.innerHTML = jobtypename;
  cell4.innerHTML = hours_perweekname;
  cell5.innerHTML = notesGlyphicon;
  cell6.innerHTML = remove_icon;


  $("#hours_perweek").val('default');
  $("#hours_perweek").selectpicker("refresh");
  $("#jobtype").val('default');
  $("#jobtype").selectpicker("refresh");
  $("#student").val('default');
  $("#student").selectpicker("refresh");
  $("#position").val('default');
  $("#position").selectpicker("refresh");

}


var total_hour_dict = {}
function checkTotalhoursTable() {//Checks if the student has enough hours to require an overload form
  var table = document.getElementById("mytable");
  var student = document.getElementById("student");
  var studentname = student.options[student.selectedIndex].text;
  var totalHours = 0
  var hours_perweek = document.getElementById("hours_perweek");
  var hours_perweekname = hours_perweek.options[hours_perweek.selectedIndex].text;
  for(const tr of table.querySelectorAll("thead tr")) {
     const td0 = tr.querySelector("td:nth-child(1)");
     const td2 = tr.querySelector("td:nth-child(4)");
     if ((td0.innerHTML == studentname)) {
       totalHours = totalHours + parseInt(td2.innerHTML);
        }
      }
  totalHours = totalHours + parseInt(hours_perweekname);
  total_hour_dict["total"] = {totalHours}
}


function checkForTotalHoursDatabase(test = "") {// gets sum of the total weekly hours from the database and add it to the ones in the table.
  var student = $("#student").val();
  var term = $("#term").val();
  var url = "/laborstatusform/gethours/" + term +"/" +student;
  $.ajax({
    url: url,
    dataType: "json",
    success: function (response){
      var total_weeklyhours_from_database = response["weeklyHours"]["Total Weekly Hours"]
      var total_weeklyhours_from_table = total_hour_dict["total"]["totalHours"]
      var total = total_weeklyhours_from_database + total_weeklyhours_from_table
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
      var studentname = student.options[student.selectedIndex].text;
      var position = document.getElementById("position");
      var positionname = position.options[position.selectedIndex].text;

      for(const tr of table.querySelectorAll("thead tr")) {
         const td0 = tr.querySelector("td:nth-child(1)");
         const td1 = tr.querySelector("td:nth-child(2)");
         const td2 = tr.querySelector("td:nth-child(3)");

         if ((td0.innerHTML == studentname) && (td1.innerHTML==positionname)) {
           document.getElementById("warningModalText").innerHTML = "Match found for " +studentname +" and " + positionname
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
  var studentname = student.options[student.selectedIndex].text;
  var position = document.getElementById("position");
  var positionname = position.options[position.selectedIndex].text;
  var posn_code = $("#position").val()
  var contracthoursname = document.getElementById("contracthours").value;
  var notesGlyphicon = "<a data-toggle='modal' onclick = 'showNotesModal(\""+String(studentname) + String(positionname)+"\")' id= '"+String(studentname) +
                                                          String(positionname)+"' ><span class='glyphicon glyphicon-edit'></span></a>";
  var remove_icon = "<a onclick = 'deleteRow(this)' class='remove'><span class='glyphicon glyphicon-remove'></span></a>";


  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  $(cell2).attr("data-posn", posn_code);
  cell2.id="position_code";
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);
  var cell5 = row.insertCell(4);

  cell1.innerHTML = studentname;
  cell2.innerHTML = positionname;
  cell3.innerHTML = contracthoursname;
  cell4.innerHTML = notesGlyphicon;
  cell5.innerHTML = remove_icon;

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
    var rowlength = document.getElementById("mytable").rows.length;
    if (rowlength > 1) {
       createModalContent();
    }
  }
  else{
    displayTable(test); // the passed argument is used to prevent plus glyphicon from submitting the form.
  }
}

function createModalContent() { // Populates Submit Modal with Student information from the table
  var test_dict = createTabledataDictionary();
  term = $("#term").val();
  var whichterm = term.toString().substr(-2);
  modal_list = [];

  if (whichterm != 11 && whichterm !=12 && whichterm !=00){
    for (var key in test_dict) {
      var student = test_dict[key]["Student"];
      var position = test_dict[key]["Position"];
      var contractHours = test_dict[key]["Contract Hours"];
      var big_string = "<li>" + student + ' | ' + position + ' | ' + contractHours;
      modal_list.push(big_string)
    }
    document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                            "<ul style='display: inline-block;text-align:left;'>" +
                                                            modal_list.join("</li>")+"</ul>"+
                                                            "<br><br>The labor status form will be eligible for approval in one business day."
    $('#SubmitModal').modal('show')
  }
  else {
    for (var key in test_dict) {
      var student = test_dict[key]["Student"];
      var position = test_dict[key]["Position"];
      var jobtype = test_dict[key]["Job Type"];
      var hours = test_dict[key]["Hours Per Week"];
      var big_string = "<li>" + student + ' | ' + position + ' | ' + jobtype + ' | ' + hours;
      modal_list.push(big_string)
    }
    document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                            "<ul style='display: inline-block;text-align:left;'>" +
                                                            modal_list.join("</li>")+"</ul>"+
                                                            "<br><br>The labor status form will be eligible for approval in one business day."
    $('#SubmitModal').modal('show')
  }
}


function createTabledataDictionary() { // puts all of the forms into dictionaries
  var list_dict_ajax = [];
  $('#mytable tr').has('td').each(function() {
    /* Get the input box values first */
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

      /* If it's a break, get table values */
      if (whichterm != 11 && whichterm !=12 && whichterm !=00) {
        tabledata_dict["Job Type"] = "Secondary";
        var headers_2_data = ["Student", "Position", "Contract Hours"];
        $('td', $(this)).each(function(index, item) {
          var a_tag = $.parseHTML($(item).html());
          if (!$(a_tag).hasClass('remove')) {
            var notes = $(a_tag).data('note');
            tabledata_dict["Supervisor Notes"] = notes;
            tabledata_dict[headers_2_data[index]] = $(item).html();
          }
        });
        list_dict_ajax.push(tabledata_dict);
        test_dict = {}
        for ( var key in list_dict_ajax){
          test_dict[key] = list_dict_ajax[key];
        }
      }
      /* If it's academic year, get the table values */
      else {
          var headers_data = ["Student", "Position", "Job Type", "Hours Per Week"];
          $('td', $(this)).each(function(index, item) {
            var a_tag = $.parseHTML($(item).html());
            if (!$(a_tag).hasClass('remove')) {
              var notes = $(a_tag).data('note');
              tabledata_dict["Supervisor Notes"] = notes;
              tabledata_dict[headers_data[index]] = $(item).html();
            }
          });
          list_dict_ajax.push(tabledata_dict);
          test_dict = {} // FIXME rename to something else, this is the dictionary that contains all the forms
          for ( var key in list_dict_ajax){
            test_dict[key] = list_dict_ajax[key];
          }
      }
     });

  delete test_dict["0"] // gets rid of the first dictionary that contains table labels
  alert(JSON.stringify(test_dict))
  return test_dict
}

// SEND DATA TO THE DATABASE
function userInsert(){
  var test_dict = createTabledataDictionary()
  data = JSON.stringify(test_dict);
  alert(data)
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
           var whichterm = term.toString().substr(-2);
           modal_list = [];
           if (response){
             for (var key in test_dict) {
               var student = test_dict[key]["Student"];
               var position = test_dict[key]["Position"];
               var contractHours = test_dict[key]["Contract Hours"];
               var jobtype = test_dict[key]["Job Type"];
               var hours = test_dict[key]["Hours Per Week"];
               if (whichterm != 11 && whichterm !=12 && whichterm !=00){
                 var big_string = "<li>" +"<span class='glyphicon glyphicon-ok' style='color:green'></span> " + student + ' | ' + position + ' | ' + contractHours;
               }
               else {
                 var big_string = "<li>"+"<span class='glyphicon glyphicon-ok' style='color:green'></span> " + student + ' | ' + position + ' | ' + jobtype + ' | ' + hours;
              }
              modal_list.push(big_string)
            }
          }

          else {
            for (var key in test_dict) {
               var student = test_dict[key]["Student"];
               var position = test_dict[key]["Position"];
               var contractHours = test_dict[key]["Contract Hours"];
               var hours = test_dict[key]["Hours Per Week"];

              if (whichterm != 11 && whichterm !=12 && whichterm !=00){
               var big_string = "<li>" +"<span class='glyphicon glyphicon-remove' style='color:red'></span> " + student + ' | ' + position + ' | ' + contractHours;
              }
              else {
                var big_string = "<li>"+"<span class='glyphicon glyphicon-remove' style='color:red'></span> " + student + ' | ' + position + ' | ' + jobtype + ' | ' + hours;
              }
              modal_list.push(big_string)
            }
           }
         document.getElementById("SubmitModalText").innerHTML = "Labor status form(s) was submitted for:<br><br>" +
                                                                 "<ul style='display: inline-block;text-align:left;'>" +
                                                                 modal_list.join("</li>")+"</ul>"+
                                                                 "<br><br>The labor status form will be eligible for approval in one business day."
         $('#SubmitModal').modal('show')
       }
     });

     $('#SubmitModal').modal({backdrop: true, keyboard: false, show: true});
     $('#SubmitModal').data('bs.modal').options.backdrop = 'static';
     document.getElementById('submitmodalid').innerHTML = "Done";
     document.getElementById('submitmodalid').onclick = function() { window.location.reload();}
}
