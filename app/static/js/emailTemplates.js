emailTemplateArray = [];

$(document).ready(function() {
  console.log("pre funct");
  getEmailArray();
  console.log("post funct");

});


function getEmailArray(){
  console.log("in funct");
  $.ajax({
    url: "/admin/emailTemplates/getEmailArray/",
    dataType: "json",
    success: function(response){
      console.log("in AJAX");
      console.log(typeof(response));
      var item = JSON.parse(response)
      console.log(typeof(item));
      console.log("---response: ", response);
      // print()
      // emailTemplateArray = JSON.parse(response);
      console.log("---array: ", emailTemplateArray)
      for(i = 0; i < emailTemplateArray.length; i++){
        // console.log("in loop:", i);
        console.log(emailTemplateArray[i]);
      }
      // console.log("---response: ", response);
      // emailTemplateArray = JSON.stringify(response);
      // console.log("---array: ", emailTemplateArray);
    }
  })
}


function populatePurpose(){
  // This function will begin by refreshing the 'Purpose' select picker everytime,
  // in order to correctly update it everytime. The function then checks what
  // recipient was choosen from the select picker, and queries all the purposes from
  // the database that correspond to that recipient, and finally appends the purposes
  // into the 'Purpose' selectpicker.
  $("#purpose").empty()
  $("#purpose").val('default').selectpicker("refresh")
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
  // This method will check what purpose is selected and what is currently
  // selected in the CKEditor body. Then on an AJAX call we send that to the
  // database to override the current body of the email template that was
  // selected. On success, we reload the page and give a python success flash message.
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
