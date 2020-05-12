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
    success:function(response){
      console.log("success", response);
    },
    error:function(response){
      console.log("error", response);
    }
  })
}
