$(document).ready(function() {
  // CKEDITOR.replace( 'editor1' );
});

function populatePurpose(){
  // alert("Hello world")
  $("#purpose").val('default').selectpicker("refresh");
  $("#purpose").empty();
  $("#subject").val("Subject")
  CKEDITOR.instances["editor1"].setData('');
  var recipient = $("#recipient").val();
  console.log(recipient);
  $.ajax({
    url: "/admin/emailTemplates/getPurpose/" + recipient,
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

function getEmailTemplate(){
  $("#subject").val("Subject")
  CKEDITOR.instances["editor1"].setData('');
  var purpose = $("#purpose").val();
  console.log(purpose);
  $.ajax({
    url: "/admin/emailTemplates/getEmail/" + purpose,
    dataType: "json",
    success: function(response){
      var body = response["emailBody"]
      var subject = response["emailSubject"]
      console.log(subject);
      CKEDITOR.instances["editor1"].insertHtml(body);
      $("#subject").val(subject)
    }
  })
}

function postEmailTemplate(){
  var body = CKEDITOR.instances.editor1.getData();
  var purpose = $("#purpose").val();
  console.log(body);
  console.log(purpose);
  $.ajax({
    url: "/admin/emailTemplates/postEmail/",
    data: { 'body': body, 'purpose': purpose },
    dataType: 'json',
    type: 'POST',
    success: function(response){
      location.reload()
    }

  })
}
