$(document).ready(function() {
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
  // alert("Hello world")
  $("#subject").val("Subject")
  CKEDITOR.instances["editor1"].setData('');
  var purpose = $("#purpose").val();
  console.log(purpose);
  $.ajax({
    url: "/admin/emailTemplates/getEmail/" + purpose,
    dataType: "json",
    success: function(response){
      console.log(response)
      var body = response["emailBody"]
      var subject = response["emailSubject"]
      console.log(subject);
      // console.log(body);
      CKEDITOR.instances["editor1"].insertHtml(body);
      $("#subject").val(subject)
      var content= CKEDITOR.instances.editor1.getData();
      console.log(content);
      // for (var key in response){
      //   var value = response[key]["Purpose"]
      //   $("#purpose").append('<option value="' + value + '">' + value + '</option>');
      //   $("#purpose").val('default').selectpicker("refresh");
      // }
    }
  })
}
