$(document).ready(function() {
});

function populatePurpose(){
  // alert("Hello world")
  $("#purpose").val('default').selectpicker("refresh");
  $("#purpose").empty();
  $("#subject").val('default').selectpicker("refresh");
  var recipient = $("#recipient").val();
  console.log(recipient);
  $.ajax({
    url: "/admin/emailTemplates/" + recipient,
    dataType: "json",
    success: function(response){
      console.log(response)
      for (var key in response){
        var value = response[key]["Purpose"]
        $("#purpose").append('<option value="' + value + '">' + value + '</option>');
        $("#purpose").val('default').selectpicker("refresh");
      }
    }
  })
}
