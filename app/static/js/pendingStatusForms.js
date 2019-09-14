
function insertApprovals() {
  var ids = [];
  var getChecked = $('input:checked').each(function() {
    ids.push(this.value);
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
      if ("Success" in response) {
        // console.log(response);
        //Clears supervisor notes p tag and the labor notes textarea
        $("#notesText").empty();
        $("#laborNotesText").empty();
      } else {
          // console.log(response);
          //Populates notes value from the database
          $("#notesText").html(response["supervisorNotes"]);
          $("#laborNotesText").html(response["laborDepartmentNotes"]);
      }
    }
  })
};



function saveLaborNotes() { // saves notes written in textarea when save button of modal is clicked
  var notesTextId = $("#dummyInput").val(); //a dummy value in order to retrieve the id
  var notesUniqueId = "notes_" + notesTextId; //
  var uniqueTextArea = "laborNotesText" + notesTextId
  console.log(notesUniqueId);
  $("#laborNotesText").val()= $(uniqueTextArea).attr("data-note");
  $("#saveNotes").attr('onclick',"saveNotes('" + uniqueTextArea +"')");

}

 function saveNotes() { // saves notes written in textarea when save button of modal is clicked
   var notes = $("#laborNotesText").val();

   console.log(notes);

   console.log($(uniqueTextArea).attr("data-note", notes));
 }

 function notesInsert() {
   notes = []
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

$("#notesModal").on('hidden.bs.modal', function(event){
  $("#notesText").empty();
  $("#laborNotesText").empty();
})

function closeNotesModal(){ //makes sure that it empties text areas and p tags when modal is closed
  $("#notesText").empty();
  $("#laborNotesText").empty();
}
