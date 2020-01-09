$(document).ready(function() {
});

function populatePurpose(){
  $("#purpose").val('default').selectpicker("refresh");
  $("#purpose").empty();
  $("#subject").val("Subject")
  CKEDITOR.instances["editor1"].setData('');
  var recipient = $("#recipient").val();
  $.ajax({
    url: "/admin/emailTemplates/getPurpose/" + recipient,
    dataType: "json",
    success: function(response){
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
  $.ajax({
    url: "/admin/emailTemplates/getEmail/" + purpose,
    dataType: "json",
    success: function(response){
      var body = response["emailBody"]
      var subject = response["emailSubject"]
      CKEDITOR.instances["editor1"].insertHtml(body);
      $("#subject").val(subject)
    }
  })
}

function postEmailTemplate(){
  var body = CKEDITOR.instances.editor1.getData();
  var purpose = $("#purpose").val();
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

function discard(){
  if ( !$("#purpose").val() ) {
    msg = "There are no changes to be discarded.";
    category = "danger";
  }
  else {
    $("#recipient").val('default').selectpicker("refresh");
    $("#purpose").val('default').selectpicker("refresh");
    $("#purpose").empty();
    $("#subject").val("Subject")
    CKEDITOR.instances["editor1"].setData('');
    msg = "The email template changes have been discarded.";
    category = "info";
  }
  $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>');
  $("#flasher").delay(3000).fadeOut();
}

function saveChanges() {
  if ( !$("#purpose").val() ) {
    msg = "There are no changes to be saved.";
    category = "danger";
    $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>');
    $("#flasher").delay(3000).fadeOut();
  }
  else{
    $("#modal").modal("show");
  }
}
