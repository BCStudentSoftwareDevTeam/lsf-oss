function openModal(FormID) {
  /*
    This function gets a response from the controller function: populateModal() in laborHistory.py.  The response is the data for the modal that pops up
    when the position is clicked.
  */
  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/' + FormID,
    success: function(response) {
      $("#holdModal").empty().append(response);
      $("#modal").modal("show");
      $("#modify").attr("href", "/modifyLSF/" + FormID); // will go to the modifyLSF controller
      console.log(FormID);
      $("#rehire").attr("href", "/laborstatusform/" + FormID); // will go to the lsf controller

      // $("#pending").attr("href", "//" + );  // IMPORTANT: This page (Modified Pendign form) has not been created yet
                                              // so make sure to have the redirect URL for it here.
      $("#release").attr("href", "/laborReleaseForm/" + FormID); // will go to labor release form controller
    }
  });
}

function withdrawform(formID){
  /*
  This funciton gets a response from the controller function: updatestatus_post() in laborHistory.py.  It reloads the page when the forms from the
  database are deleted by the controller function.
  */
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
