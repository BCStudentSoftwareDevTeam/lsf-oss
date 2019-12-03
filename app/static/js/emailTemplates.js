$(document).ready(function() {
});

function populatePurpose(){
  // alert("Hello world")
  $("#purpose").val('default').selectpicker("refresh");
  $("#subject").val('default').selectpicker("refresh");
  var recipient = $("#recipient").val();
  console.log(recipient);
  $.ajax({
    url: "/admin/emailTemplates/" + recipient,
    dataType: "json",
    success: function(response){

    }
  })
}
