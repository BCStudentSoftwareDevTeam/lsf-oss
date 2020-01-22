$('#positionTable tbody tr  td').on('click',function(){
     $("#modal").modal("show");
     $("#modal").find('.modal-content').load('/laborHistory/modal/' + this.id)
     setTimeout(function(){ $(".loader").fadeOut("slow"); }, 500);
});

function redirection(laborStatusKey){
  /*
  When any of the three buttons is clicked, this function will append the 'href' attribute with the
  correct redirection link and LSF primary key to each button.
  */
  $("#modify").attr("href", "/modifyLSF/" + laborStatusKey); // will go to the modifyLSF controller
  $("#rehire").attr("href", "/laborstatusform/" + laborStatusKey); // will go to the lsf controller
  $("#release").attr("href", "/laborReleaseForm/" + laborStatusKey); // will go to labor release form controller
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
