$(document).ready( function(){
    $('#pendingForms, #statusForms, #modifiedForms, #overloadForms, #releaseForms').DataTable({
        'columnDefs': [{ 'orderable': false, 'targets': [0,4,10]}], // hide sort icon on header of first column
        // 'columnDefs': [{ 'orderable': false, 'targets': 9 }],
        'aaSorting': [[1, 'asc']], // start to sort data in second column
        pageLength: 10
        // "dom": '<"top"fl>rt<"bottom"p><"clear">'

    });
});

// $(document).ready( function(){
//     $('#modifiedForms').DataTable({
//         'columnDefs': [{ 'orderable': false, 'targets': [0,4,10]}], // hide sort icon on header of first column
//         // 'columnDefs': [{ 'orderable': false, 'targets': 9 }],
//         'aaSorting': [[1, 'asc']], // start to sort data in second column
//         pageLength: 10


var labor_details_ids = []; // for insertApprovals() and final_approval() only
function insertApprovals() {
  var getChecked = $('input:checked').each(function() {
    labor_details_ids.push(this.value);
  })

  //this checks wether the checkbox is checked or not and if does not it disable the approve selected button
  var atLeastOneIsChecked = $('input[name="check[]"]:checked').length > 0;
  if (!atLeastOneIsChecked){
    $("#approveSelected").prop("disabled",true);
    location.reload();
       }
    data = JSON.stringify(labor_details_ids);
   $.ajax({
     type: "POST",
     url: "/admin/checkedForms",
     datatype: "json",
     data: data,
     contentType: 'application/json',
     success: function(response){
       if (response){
         returned_details = response;
         updateApproveTableData(returned_details);
         // updateDenialTableData(returned_details);
              }
            }
          })
      };
//this method adds data to each row in the approve selected Modal
function updateApproveTableData(returned_details){
  for (var i = 0; i < returned_details.length; i++){
    var student=returned_details[i][0]
    var position= returned_details[i][1]
     var r_hour= returned_details[i][3]
     var c_Hours= returned_details[i][4]
     // console.log(c_Hours,"jamalito")
      var supervisor= returned_details[i][2]
      var hours = " "
      if (r_hour.length==4){
        hours = c_Hours
      }
      else {
        hours = r_hour
      }
      $('#classTable').append('<tr><td>'+student+'</td><td>'+position+'</td><td> '+hours+'</td> <td> '+supervisor+'</td></tr>');

        }
      }

function finalApproval() { //this method changes the status of the lsf from pending to approved status
  data = JSON.stringify(labor_details_ids);
  $.ajax({
    type: "POST",
    url: "/admin/finalApproval",
    datatype: "json",
    data: data,
    contentType: 'application/json',
    success: function(response){
      if (response){
        console.log('success', response["success"]);
        if(response["success"]) {
            location.reload(true);
        }
       }
     }
   })
 };

labor_denial_id=[]; //this arrary is for insertDenial() and finalDenial() methods
//This method calls AJAX from checkforms methods in the controller
function insertDenial(val){
    labor_denial_id.push(val);
    data = JSON.stringify(labor_denial_id);
    // console.log("data :", data)
   $.ajax({
     type: "POST",
     url: "/admin/checkedForms",
     datatype: "json",
     data: data,
     contentType: 'application/json',
     success: function(response){
       if (response){
         labor_denial_detials = response;
         // location.reload(true);
         finalDenial_data(labor_denial_detials);
        }
      }
    })
};

// this method inserts data to the table of denial popup modal
function finalDenial_data(returned_details){
  for (var i = 0; i < returned_details.length; i++){
    var student=returned_details[i][0]
    var position= returned_details[i][1]
     var r_hour= returned_details[i][3]
     var c_Hours= returned_details[i][4]
     console.log(c_Hours,"jamalito")
      var supervisor= returned_details[i][2]
      var hours = " "
      if (r_hour.length==4){
        hours = c_Hours
      }
      else {
        hours = r_hour
      }
      $('#denyTable').append('<tr><td>'+student+'</td><td>'+position+'</td><td> '+supervisor+'</td> <td> '+ hours +'</td></tr>');
        }
      }

 function finalDenial() {// this mehod is AJAX call for the finalDenial method in python file
   data = JSON.stringify(labor_denial_id);
   $.ajax({
     type: "POST",
     url: "/admin/finalDenial",
     datatype: "json",
     data: data,
     contentType: 'application/json',
     success: function(response){
       if (response){
         console.log('success', response["success"]);
         if(response["success"]) {
             location.reload(true);
              }
            }
          }
        })
      };

function getNotes (formId) {
  console.log(formId);

  $.ajax({
    type: "GET",
    url: "/admin/getNotes/"+formId,
    datatype: "json",
    success: function (response) {

      if ("Success" in response && response["Success"] == "false") {
        //Clears supervisor notes p tag and the labor notes textarea
        console.log("This is why it failed: ", response);
        $("#notesText").empty();
        $("#laborNotesText").empty();

       } else {
          $("#laborNotesText").data('formId',formId) //attaches the formid data to the textarea
          //Populates notes value from the database

          if ("supervisorNotes" in response) {
            $("#notesText").html(response["supervisorNotes"]);
            console.log(response);
             }

          if ("laborDepartmentNotes" in response) {
            $("#laborNotesText").html(response["laborDepartmentNotes"]);
            console.log(response);
            console.log(response["laborDepartmentNotes"]);
            }
         }
       }
   })
};

 function notesInsert() {
   var formId = $("#laborNotesText").data('formId');
   var laborNotes = $("#laborNotesText").val(); //this is getting the id of the labor notes text area
   var notes = {'formId': formId, 'notes':laborNotes};   // {ID: textarea value} this sets the text area to what the user types in it

   var formId = notes.formId; //This is how we get the ID of the form
   var note = notes.notes; //This is how we are getting the note object from the dictionary

   data = JSON.stringify(note);

    var notesGlyph = $("#notes_" + formId);

   $("#saveNotes").on('submit', function(e) {
     e.preventDefault();
     });

       $.ajax({
          method: "POST",
          url: '/admin/notesInsert/'+ formId,
          data: data,
          contentType: 'application/json',
          success: function(response) {
            if (response){
              //This changes the color of the notes glyphicon when a labor note is saved
              if ($(notesGlyph).hasClass("text-success")) {
                  $(notesGlyph).removeClass("text-success");
                  $(notesGlyph).addClass("text-danger");
                }
              else if ($(notesGlyph).hasClass("text-secondary")) {
                $(notesGlyph).removeClass("text-secondary");
                $(notesGlyph).addClass("text-danger");
                }
                window.location.reload(true);
              }
          }
        });
     }

function createTabledataDictionary() { // puts all of the forms into dictionaries
  var listDictAJAX = [];
  $('#statusForms tr').has('td').each(function() {
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

  delete allTableDataDict["0"] // gets rid of the first dictionary that contains table labels
  return allTableDataDict
}

function clearTextArea(){ //makes sure that it empties text areas and p tags when modal is closed
  $("#notesText").empty();
  $("#laborNotesText").empty();
}
