$(document).ready(function() {
  // If the overload tab has been selected, then we need to restrict the
  // ordering functionality on different headers
  if($('#overloadTab').hasClass('active')){
    targetsList = [8]
  } else {
    targetsList = [0, 9]
  }
  // If overload tab has been clicked, then we
  $('#pendingForms, #statusForms, #modifiedForms, #releaseForms').DataTable({
    'columnDefs': [{
      'orderable': false,
      'targets': targetsList
    }], // hide sort icon on header of first column
    // 'columnDefs': [{ 'orderable': false, 'targets': 9 }],
    'aaSorting': [
      [1, 'asc']
    ], // start to sort data in second column
    pageLength: 50
    // "dom": '<"top"fl>rt<"bottom"p><"clear">'
  });
});

var labor_details_ids = []; // for insertApprovals() and final_approval() only
function insertApprovals() {
  var getChecked = $('input:checked').each(function() {
    labor_details_ids.push(this.value);
    });

  //this checks wether the checkbox is checked or not and if does not it disable the approve selected button
  var atLeastOneIsChecked = $('input[name="check[]"]:checked').length > 0;
  if (!atLeastOneIsChecked) {
    $("#approveSelected").prop("disabled", true);
    $("#approvePendingForm").prop("disabled", true);
    $("#modifiedApproval").prop("disabled", true);
    $("#approveOverload").prop("disabled", true);
    $("#approveRelease").prop("disabled", true);

    location.reload();
  }
  var data = JSON.stringify(labor_details_ids);
  $.ajax({
    type: "POST",
    url: "/admin/checkedForms",
    datatype: "json",
    data: data,
    contentType: 'application/json',
    success: function(response) {
      if (response) {
        var returned_details = response;
        updateApproveTableData(returned_details);
      }
    }
  });
}
//this method adds data to each row in the approve selected Modal
function updateApproveTableData(returned_details) {
  for (var i = 0; i < returned_details.length; i++) {
    var student = returned_details[i][0];
    var position = returned_details[i][1];
    var r_hour = returned_details[i][3];
    var c_Hours = returned_details[i][4];
    var supervisor = returned_details[i][2];
    var hours = " ";
    if (r_hour.length == 4) {
      hours = c_Hours;
    } else {
      hours = r_hour;
    }
    $('#classTableBody').append('<tr><td>' + student + '</td><td>' + position + '</td><td> ' + hours + '</td> <td> ' + supervisor + '</td></tr>');
  }
}

function approvalModalClose(){// on close of approval modal we are clearing the table to prevent duplicate data.
  $('#classTableBody').empty();
  labor_details_ids = [] // emptying the list, becuase otherwise will cause duplicate data.
}

function finalApproval() { //this method changes the status of the lsf from pending to approved status
  var data = JSON.stringify(labor_details_ids);
  $.ajax({
    type: "POST",
    url: "/admin/updateStatus/approved",
    datatype: "json",
    data: data,
    contentType: 'application/json',
    success: function(response) {
      if (response) {
        if (response.success) {
          location.reload(true);
        }
      }
    }
  });
}

var laborDenialInfo = []; //this arrary is for insertDenial() and finalDenial() methods
//This method calls AJAX from checkforms methods in the controller
function insertDenial(val) {
  laborDenialInfo.push(val);
  var data = JSON.stringify(laborDenialInfo);
  $.ajax({
    type: "POST",
    url: "/admin/checkedForms",
    datatype: "json",
    data: data,
    contentType: 'application/json',
    success: function(response) {
      if (response) {
        var labor_denial_detials = response;
        finalDenial_data(labor_denial_detials);
      }
    }
  });
}

// this method inserts data to the table of denial popup modal
function finalDenial_data(returned_details) {
  for (var i = 0; i < returned_details.length; i++) {
    var student = returned_details[i][0];
    var position = returned_details[i][1];
    var r_hour = returned_details[i][3];
    var c_Hours = returned_details[i][4];
    var supervisor = returned_details[i][2];
    var hours = " ";
    if (r_hour.length == 4) {
      hours = c_Hours;
    } else {
      hours = r_hour;
    }
    $('#denialPendingFormsBody').append('<tr><td>' + student + '</td><td>' + position + '</td><td> ' + supervisor + '</td> <td> ' + hours + '</td></tr>'); //populate the denial modal for all pending forms
  }
}

function denialModalClose(){// on close of approval modal we are clearing the table to prevent duplicate data.
  $('#denialPendingFormsBody').empty();
  laborDenialInfo = [] // emptying the list, becuase otherwise will cause duplicate data.
}

function finalDenial() { // this mehod is AJAX call for the finalDenial method in python file
  var data = JSON.stringify(laborDenialInfo);
  $.ajax({
    type: "POST",
    url: "/admin/updateStatus/denied",
    datatype: "json",
    data: data,
    contentType: 'application/json',
    success: function(response) {
      if (response) {
        if (response.success) {
          location.reload(true);
        }
      }
    }
  });
}

function getNotes(formId) {
  $.ajax({
    type: "GET",
    url: "/admin/getNotes/" + formId,
    datatype: "json",
    success: function(response) {
      if ("Success" in response && response.Success == "false") {
        //Clears supervisor notes p tag and the labor notes textarea
        $(".notesText").empty();
        $("#laborNotesText").empty();
      } else {
        $("#laborNotesText").data('formId', formId); //attaches the formid data to the textarea

        //Populates notes value from the database
        if ("supervisorNotes" in response) {
          $(".supeNotesLabel").show()
          $(".notesText").show()
          $(".notesText").html(response.supervisorNotes);
        }
        if (!("supervisorNotes" in response)) {
          $(".supeNotesLabel").hide()
          $(".notesText").hide()
        }
        if ("laborDepartmentNotes" in response) {
          $(".notesLogArea").html(response.laborDepartmentNotes);
        } else if (!("laborDepartmentNotes" in response)) {
          $(".notesLogArea").html("No notes to show")
        }
      }
    }
  });
}

function notesInsert(textareaID, buttonID) {
  var formId = $("#" + textareaID).data('formId');
  var laborNotes = $("#" + textareaID).val(); //this is getting the id of the labor notes text area
  var notes = {
    'formId': formId,
    'notes': laborNotes
  }; // {ID: textarea value} this sets the text area to what the user types in it
  formId = notes.formId; //This is how we get the ID of the form
  var note = notes.notes; //This is how we are getting the note object from the dictionary
  var data = JSON.stringify(note);
  var notesGlyph = $("#notes_" + formId);

  $("#" + buttonID).on('submit', function(e) {
    e.preventDefault();
  });

  $.ajax({
    method: "POST",
    url: '/admin/notesInsert/' + formId,
    data: data,
    contentType: 'application/json',
    success: function(response) {
      if (response) {
        //This changes the color of the notes glyphicon when a labor note is saved
        if ($(notesGlyph).hasClass("text-success")) {
          $(notesGlyph).removeClass("text-success");
          $(notesGlyph).addClass("text-danger");
        } else if ($(notesGlyph).hasClass("text-secondary")) {
          $(notesGlyph).removeClass("text-secondary");
          $(notesGlyph).addClass("text-danger");
        }
        window.location.reload(true);
      }
    }
  });
}

function finalDeny() {
  /*
  This method will first check if the deny reason text area has been populated, and if
  it is then the method to update the form with the reject reason will be called
  */
  var denyReason = $('#denyReason').val()
  if (denyReason == '') {
    $('#denyReason').attr("placeholder", 'A reason for denial is required to deny the form')
    $('#denyReason').css('border-color', 'red');
  } else {
    laborDenialInfo.push(denyReason)
    finalDenial();
  }
}

function createTabledataDictionary() { // puts all of the forms into dictionaries
  var listDictAJAX = [];
  $('#statusForms tr').has('td').each(function() {
    /* Get the input box values first */
    var supervisor = $("#selectedSupervisor").val();
    var department = $("#selectedDepartment").val();
    var term = $("#selectedTerm").val();
    var whichTerm = term.toString().substr(-2);
    var startDate = $("#dateTimePicker1").val();
    var endDate = $("#dateTimePicker2").val();
    var positionCode = $("#position_code").attr("data-posn");
    var listDict = [];
    listDict.push(supervisor, department, term, startDate, endDate, positionCode);
    var headersLabel = ["Supervisor", "Department", "Term", "Start Date", "End Date", "Position Code"];
    var tableDataDict = {};
    for (var i in listDict) {
      tableDataDict[headersLabel[i]] = listDict[i];
    }

    /* If it's a break, get table values */
    if (whichTerm != 11 && whichTerm != 12 && whichTerm != 00) {
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
      var allTableDataDict = {};
      for (var key in listDictAJAX) {
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
      var allTableDataDict = {}; // this is the dictionary that contains all the forms
      for (var key in listDictAJAX) {
        allTableDataDict[key] = listDictAJAX[key];
      }
    }
  });

  delete allTableDataDict["0"]; // gets rid of the first dictionary that contains table labels
  return allTableDataDict;
}

function clearTextArea() { //makes sure that it empties text areas and p tags when modal is closed
  $("#notesText").empty();
  $("#laborNotesText").empty();
}


function loadOverloadModal(formHistoryID, laborStatusFormID) {
  /*
  This method sends an AJAX call to recieve data used to populate
  the overload modal.
  */
  var laborOverloadID = []
  laborOverloadID.push(formHistoryID);
  var data = JSON.stringify(laborOverloadID);
  $.ajax({
    type: "POST",
    url: "/admin/overloadModal",
    datatype: "json",
    data: data,
    contentType: 'application/json',
    success: function(response) {
      if (response) {
        var studentName = response['stuName']
        var position = response['stuPosition']
        var department = response['stuDepartment']
        var supervisor = response['stuSupervisor']
        var hours = response['stuHours']
        var overloadReason = response['studentOverloadReason']
        var emailDateSAAS = response['SAASEmail']
        var statusSAAS = response['SAASStatus']
        var emailDateFinancialAid = response['financialAidLastEmail']
        var statusFinancialAid = response['financialAidStatus']
        $('#studentOverloadReason').append(overloadReason)
        $('#overloadStudentTable').append('<tr><td>' + studentName + '</td><td>' + position + '</td><td>' + hours + '</td><td>' + supervisor + '</td><td>' + department + '</td></tr>'); //populate the denial modal for all pending forms
        $('#overloadStudentTable').append('<tr><td><strong>Overload Reason</strong></td><td colspan="4">' + overloadReason + '</td></tr>')
        $('#overloadDepartmentTable').append('<tr><td>SAAS</td><td id="statusSAAS">' + statusSAAS + '</td><td id="emailSAAS">' + emailDateSAAS + '</td><td><button id="SAASEmail" value=' + formHistoryID + ' type="button" class ="btn btn-info" onclick="sendEmail(this.value, this.id)">Send Email</button></td></tr>');
        $('#overloadDepartmentTable').append('<tr><td>Financial Aid</td><td id="statusFinancialAid">' + statusFinancialAid + '</td><td id="emailFinancialAid">' + emailDateFinancialAid + '</td><td><button id="financialAidEmail" value=' + formHistoryID + ' type="button" class ="btn btn-info" onclick="sendEmail(this.value, this.id)">Send Email</button></td></tr>');
        $('#overloadNotes').data('formId', laborStatusFormID)
      }
    },
    error: function(request,status,error){
      console.log(request.responseText);
    }
  });
}

function displayModalTextArea(radioValue) {
  /*
  This method toggles the 'Deny' and 'Admin Notes' textareas
  based on what radio has been selected
  */
  var radioVal = radioValue
  if (radioVal == 'deny') {
    $('#overloadNotes').val('');
    $('#denyTextArea').css('display', 'block')
    $('#notesTextArea').css('display', 'none')

  } else {
    $('#denyOverloadReason').val('');
    $('#denyTextArea').css('display', 'none')
    $('#notesTextArea').css('display', 'block')
  }
}

function sendEmail(formHistoryID, emailRecipient) {
  /*
  This method sends data to the backend that it used to send an email,
  and also updates the data inside of the overload modal
  */
  emailTrackerInfo = {'formHistoryID': formHistoryID, 'emailRecipient': emailRecipient}
  data = JSON.stringify(emailTrackerInfo)
  $.ajax({
    method: "POST",
    url: '/admin/sendVerificationEmail',
    data: data,
    contentType: 'application/json',
    success: function(response) {
      var newDate = response['emailDate']
      var status = response['status']
      var recipient = response['recipient']
      if(recipient == 'SAAS'){
        $("#statusSAAS").html(status)
        $("#emailSAAS").html(newDate)
      }
      else if (recipient == 'Financial Aid') {
        $("#statusFinancialAid").html(status)
        $("#emailFinancialAid").html(newDate)
      }
    },
    error: function(request,status,error){
      console.log(request.responseText);
    }
  });
}

function submitOverload(formHistoryID) {
  /*
  This method is used to check if the form is ready for submission, then
  makes an AJAX call with the information needed to complete the submission
  */
  if ($('input[name=decision]:checked').length > 0) {
    var createAJAX = true
    var status = 'Pending'
    var overloadModalInfo = {'formHistoryID': formHistoryID}
    if ($('#deny').is(':checked')) {
      if($("#denyOverloadReason").val() == ""){
      $("#denyOverloadReason").focus();
      $("#required-error").show();
        createAJAX = false
      } else {
        $('#required-error').hide();
        status = 'Denied'
        var denyReason = $('#denyOverloadReason').val()
        overloadModalInfo['denialReason'] = denyReason;
      }
    } else {
      if ($('#approve').is(':checked')) {
        status = 'Approved'
      }
      if ($('#approveRel').is(':checked')) {
        status = 'Approved Reluctantly'
      }
      if ($('#overloadNotes').val() != '') {
        var adminNotes = $('#overloadNotes').val()
        overloadModalInfo['adminNotes'] = adminNotes;
      }
    }
    if (createAJAX == true) {
      overloadModalInfo['status'] = status;
      var data = JSON.stringify(overloadModalInfo)
      $.ajax({
        method: "POST",
        url: '/admin/overloadFormUpdate',
        data: data,
        contentType: 'application/json',
        success: function(response) {
          location.reload();
        },
        error: function(request,status,error){
          console.log(request.responseText);
        }
      });
    }
  } else {
    $('#radioDiv').css('border', 'thin dotted red')
    $('#radioDiv').delay(2000).queue(function(next) {
      $(this).css('border', 'none');
      next();
    })

  }
}

function toggleNotesLog(laborStatusFormID) {
  /*
  This method toggles the 'Notes' log at the bottom of the
  modal to show/hide it
  */
  if ($('#logNotesDiv').css('display') == 'none') {
    getNotes(laborStatusFormID)
    $('#logNotesDiv').css('display', 'block')
  } else {
    $('#logNotesDiv').css('display', 'none')
  }
}
