function openModal(formID) {
  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/' + laborStatusKey,
    success: function(response) {
      $("#holdModal").empty().append(response);
      $("#modal").modal("show");
      $("#modify").attr("href", "/modifyLSF/" + laborStatusKey); // will go to the modifyLSF controller
      console.log(laborStatusKey);
      $("#rehire").attr("href", "/laborstatusform/" + laborStatusKey); // will go to the lsf controller

      // $("#pending").attr("href", "//" + );  // IMPORTANT: This page (Modified Pendign form) has not been created yet
                                              // so make sure to have the redirect URL for it here.
      $("#release").attr("href", "/laborReleaseForm/" + laborStatusKey); // will go to labor release form controller
      // TODO: ON "Withdraw" button add a flash that the form has been deleted.
    }
  });
}

function withdrawform(formID){
  console.log(formID)
  formIdDict={}
  formIdDict["FormID"] = formID
  data = JSON.stringify(formIdDict);
  $.ajax({
         method: "POST",
         url: '/laborHistory/modal/updatestatus',
         data: data,
         contentType: 'application/json',
         success: function(response) {
             if (response["Success"]) {
               window.location.href = response["url"]
             }
           }
         });
       }
