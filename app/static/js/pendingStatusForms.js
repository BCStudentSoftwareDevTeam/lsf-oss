
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
      if (!("Success" in response)) {
        console.log(response);
        console.log(response["supervisorNotes"])
        // var testingText = document.createTextNode("This is a test for the p tag")

        console.log($("#notesText").html(response["supervisorNotes"]));
        $("#notesText").html(response["supervisorNotes"]);

      } else {
            $("#notesText").empty();
            }
    }
  })
};



function saveLaborNotes() { // saves notes written in textarea when save button of modal is clicked
  var notesTextId = $("#dummyInput").val();
  var notesUniqueId = "notes_" + notesTextId;
  console.log(notesUniqueId);
  document.getElementById("laborNotesText").value=document.getElementById(notesUniqueId).getAttribute("data-note");
  document.getElementById("saveNotes").setAttribute('onclick',"saveNotes('" + notesUniqueId +"')");
  console.log(idDummyInput);
}

 function saveNotes() { // saves notes written in textarea when save button of modal is clicked
   var notes = document.getElementById("laborNotesText").value;
   document.getElementById(notesTextId).setAttribute("data-note", notes);
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
