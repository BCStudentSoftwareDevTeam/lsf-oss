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

// $("#notesModal").on('hidden.bs.modal', function(event){ //this is supposed to clear the modal even if the user doesn not click the "closed" button, pero it does not work
//   $("#notesText").val('');
//   $("#laborNotesText").val('');
// })

function clearTextArea(){ //makes sure that it empties text areas and p tags when modal is closed
  $("#notesText").empty();
  $("#laborNotesText").empty();
}
