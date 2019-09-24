
function insertApprovals() { //gets only the forms that the user has checked
  var ids = [];
  var getChecked = $('input:checked').each(function() {
    ids.push(this.value); //gets the ids of checked forms
    console.log(ids);
  })
  data = JSON.stringify(ids);

 $.ajax({
   type: "POST",
   url: "/admin/checkedForms",
   datatype: "json",
   data: data,
   contentType: 'application/json',
   success: function(response){
     if (response){
       console.log(response);
   }
 }
 })
};

function getNotes (formID) {
  console.log(formID);

  $.ajax({
    type: "GET",
    url: "/admin/getNotes/"+formID,
    datatype: "json",
    success: function (response) {
      if ("Success" in response && response["Success"] == "false") {
        // console.log(response);
        //Clears supervisor notes p tag and the labor notes textarea
        $("#notesText").empty();
        $("#laborNotesText").empty();
      } else {
          // console.log(response);
          //Populates notes value from the database
          $("#laborNotesText").data('formID',formID)
          $("#notesText").html(response["supervisorNotes"]);
          $("#laborNotesText").html(response["laborDepartmentNotes"]);
      }
    }
  })
};

// function saveLaborNotes() { // saves notes written in textarea when save button of modal is clicked
//   var notesTextId = $("#dummyInput").val(); //a dummy value in order to retrieve the id
//   var notesUniqueId = "notes_" + notesTextId; //
//   var uniqueTextArea = "laborNotesText" + notesTextId
//
//   $("#saveNotes").attr('onclick',"saveNotes('" + uniqueTextArea +"')");
//
// }

 function notesInsert() {
   console.log("notesInsert")
   console.log(formID)
   var formID = $("#laborNotesText").data('formID');
   var laborNotes = $("#laborNotesText").val(); //this is getting the id of the labor notes text area
   var notes = {'formID': formID, 'notes':laborNotes};
     console.log(notes);
  //this sets the text area to what the user types in it


   data = JSON.stringify(notes);
   $("#saveNotes").on('submit', function(e) {
     e.preventDefault();
     });

   $.ajax({
          method: "POST",
          url: '/laborstatusform/notesInsert',
          data: notes,
          contentType: 'application/json',
          success: function(response) {
            console.log(response);
          }
        });
}

$("#notesModal").on('hidden.bs.modal', function(event){ //this is supposed to clear the modal even if the user doesn not click the "closed" button, pero it does not work
  $("#notesText").empty();
  $("#laborNotesText").empty();
})

function closeNotesModal(){ //makes sure that it empties text areas and p tags when modal is closed
  $("#notesText").empty();
  $("#laborNotesText").empty();
}
