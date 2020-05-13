function denialSubmission(formHistoryKey){
  // this function will update the notes and status in the db
  console.log("in denial submission");
  console.log(formHistoryKey, "formHistoryKey");
  var notesContent = $("#denyReason_"+formHistoryKey).val()
  console.log(notesContent, "deny note content");
  denialInfoDict = {}
  denialInfoDict["formHistoryID"] = formHistoryKey
  denialInfoDict["denialNote"] = notesContent
  console.log(denialInfoDict, "DenialDict");
  data = JSON.stringify(denialInfoDict)
  $.ajax({
    method: "POST",
    url:"/admin/financialAidOverloadApproval/denial",
    datatype: "json",
    data: data,
    contentType: "application/json",
    success:function(){
      console.log("success");
      msgFlash("Your changes have been saved successfuly.(You will be redirected shortly.)", "success")
      setTimeout(function() { // executed after 1 second
         window.location.replace('http://berea.edu'); // redirects to a new website
       }, 5000);
    },
    error:function(response){
      console.log("error", response);
    }
  })
}

// for showing different messages with flash
function msgFlash(flash_message, status){
    if (status === "success") {
        category = "success";
        $("#flash_container").prepend("<div class=\"alert alert-"+ category +"\" role=\"alert\" id=\"flasher\">"+flash_message+"</div>");
        $("#flasher").delay(5000).fadeOut();
    }
    else {
        category = "danger";
        $("#flash_container").prepend("<div class=\"alert alert-"+ category +"\" role=\"alert\" id=\"flasher\">"+flash_message+"</div>");
        $("#flasher").delay(5000).fadeOut();
    }

}
