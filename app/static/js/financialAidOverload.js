function overloadSubmission(formHistoryKey){
  // this function will update the notes and status in the db
  var notesContent = $("#denyReason_"+formHistoryKey).val()
  denialInfoDict = {}
  denialInfoDict["formHistoryID"] = formHistoryKey
  denialInfoDict["denialNote"] = notesContent
  data = JSON.stringify(denialInfoDict)

  if($(".textarea-required").prop("required") == true && notesContent == " "){
    $("#finOverloadSubmit").removeAttr("data-dismiss")
    $(".textarea-required").focus();
    $("#required-error").show();
  }
  else{
    $("#required-error").hide();
    $("#finOverloadSubmit").attr("data-dismiss", "modal")
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
    });
  }
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

function openApproveDenyModal(status){
  if (status == "approved"){
    $("#required-error").hide();
    $("#finOverloadSubmit").attr("data-dismiss", "modal")
    $("#finOverloadModal .modal-title").text("Reason for Approval")
    $("#modal-body-content").text("You have selected 'Approve' for this student's Overload Request. Please indicate a reasoning for this decision (Optional).");
    $(".textarea-required").prop('required', false);
    $("#finOverloadModal").modal("show");
  }
  else{
    $("#finOverloadModal .modal-title").text("Reason for Denial");
    $("#modal-body-content").text("You have selected 'Deny' for this student's Overload Request. Please indicate a reasoning for this decision");
    $(".textarea-required").prop('required', true);
    $("#finOverloadModal").modal("show");
  }
}
