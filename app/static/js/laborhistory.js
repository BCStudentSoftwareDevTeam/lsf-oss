function openModal(laborStatusKey) {
  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/' + laborStatusKey,
    success: function(response) {
      $("#holdModal").empty().append(response);
      $("#modal").modal("show");
      $("#modify").attr("href", "/modifyLSF/" + laborStatusKey); // will go to the modifyLSF controller
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
               msg = "Selected overload form has been withdrawn.";
               category = "danger";
               $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>');
               $("#flasher").delay(4000).fadeOut();
               setTimeout(location.reload.bind(location), 1000);
               return;
             }
           }
         });
       }
