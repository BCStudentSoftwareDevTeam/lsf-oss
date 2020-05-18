var emailTemplateArray;

$(document).ready(function() {
  getEmailArray();
});

function getEmailArray(){
  $.ajax({
    url: "/admin/emailTemplates/getEmailArray/",
    dataType: "json",
    success: function(response){
      emailTemplateArray = response;
    }
  })
}

function populateFormType(){
  // populates Form Type only when Recipient is selected
  $("#formType").prop("disabled", false);
  $("#formType").empty();
  $("#action").empty();
  $("#formType").empty();
  var recipient = $("#recipient").val();
  var appendedItems = [];
  for (var dict in emailTemplateArray){
    var value = emailTemplateArray[dict]["formType"];
    if(recipient == emailTemplateArray[dict]["audience"] && !appendedItems.includes(value)){
      appendedItems.push(value);
      $("#formType").append('<option value="' + value + '">' + value + '</option>');
    }
  }
  $("#formType").selectpicker("refresh");
  $("#action").selectpicker("refresh");
  $("#action").prop("disabled", true);
}

function populateAction(){
  // populates Action only when Form Type is selected
  $("#action").prop("disabled", false);
  $("#action").empty();
  var recipient = $("#recipient").val();
  var formType = $("#formType").val();
  var appendedItems = [];
  for (var dict in emailTemplateArray){
    var value = emailTemplateArray[dict]["action"];
    if(recipient == emailTemplateArray[dict]["audience"] && formType == emailTemplateArray[dict]["formType"] && !appendedItems.includes(value)){
      appendedItems.push(value);
      $("#action").append('<option value="' + value + '">' + value + '</option>');
    }
  }
  $("#action").selectpicker("refresh");
}

function populatePurpose(){
  // This function will begin by refreshing the 'Purpose' select picker everytime,
  // in order to correctly update it everytime. The function then checks what
  // recipient was choosen from the select picker, and queries all the purposes from
  // the database that correspond to that recipient, and finally appends the purposes
  // into the 'Purpose' selectpicker.
  $("#purpose").prop("disabled", false);
  $("#purpose").empty()
  $("#purpose").selectpicker("refresh")
  $("#subject").val("Subject")
  CKEDITOR.instances["editor1"].setData('')
  var recipient = $("#recipient").val()
  var formType = $("#formType").val()
  var action = $("#action").val()
  fieldsDict = {recipient: recipient,
                formType: formType,
                action: action};

  fieldsDictSTR = JSON.stringify(fieldsDict);
  $.ajax({
    url: "/admin/emailTemplates/getPurpose/" + fieldsDictSTR,
    dataType: "json",
    success: function(response){
      var value;
      for (var key in response){
        value = response[key]["Purpose"]
        $("#purpose").append('<option value="' + value + '">' + value + '</option>');
      }
      if (response.length == 1){     // if there is only 1 item left in the Purpose dropdown, choose it automatically
        $('#purpose').val(value);
        $("#purpose").selectpicker("refresh");
        getEmailTemplate();
      }
    }
  })
}

function getEmailTemplate(){
  // This method starts by clearing the subject and the body on the UI. Once that
  // is completed, this method will call the purpose. The purpose is used to pull
  // the subject and body from the appropriate template in the database and
  // fill them in the purpose selectpicker and the CKEditor body.
  CKEDITOR.instances["editor1"].setData('');
  var purpose = $("#purpose").val();
  fieldsDict = {"action": $("#action").val(),
                "formType":$("#formType").val(),
                "recipient":$("#recipient").val()
               };
  fieldsDictSTR = JSON.stringify(fieldsDict);
  $.ajax({
    url: "/admin/emailTemplates/getEmail/" + fieldsDictSTR,
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
  // This method will check what purpose is selected and what is currently
  // selected in the CKEditor body. Then on an AJAX call we send that to the
  // database to override the current body of the email template that was
  // selected. On success, we reload the page and give a python success flash message.
  var body = CKEDITOR.instances.editor1.getData();
  var purpose = $("#purpose").val();
  var action = $("#action").val();
  var formType = $("#formType").val();
  var recipient = $("#recipient").val();
  $.ajax({
    url: "/admin/emailTemplates/postEmail",
    data: { 'body': body, 'purpose': purpose, 'action': action, 'formType': formType, 'recipient': recipient},
    dataType: 'json',
    type: 'POST',
    success: function(response){
      location.reload()
    }
  })
}

function discard(){
  // This method first checks to see if a purpose was selected or not. If no
  // purpose was selected, it will flash an error message saying there were no
  // changes to be discarded. If a purpose was selected, the method will clear all
  // three selectpickers and the CKEditor body.
  if ( !$("#purpose").val() ) {
    msg = "There are no changes to be discarded.";
    category = "danger";
  }
  else {
    $("#recipient").val('default').selectpicker("refresh")
    $("#purpose").empty()
    $("#purpose").val('default').selectpicker("refresh")
    // $("#purpose").empty()
    // $("#purpose").remove()
    // $("#purpose").selectpicker('destroy')
    $("#subject").val("Subject")
    CKEDITOR.instances["editor1"].setData('')
    msg = "The email template changes have been discarded.";
    category = "info";
    console.log($("#recipient").val());
  }
  $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>');
  $("#flasher").delay(3000).fadeOut();
}

function saveChanges() {
  // This method checks to see if a purpose was selected or not. If no purpose
  // was selected, it will flash an error message saying there were no changes
  // to be discarded. If a purpose was selected, the method will call a modal that
  // will ask the user if they are sure they want to save their changes.
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
