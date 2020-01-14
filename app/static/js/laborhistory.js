$('#positionTable tbody tr  td').on('click',function(){
     $("#modal").modal("show");
     $("#modal").find('.modal-content').load('/laborHistory/modal/' + this.id)
     setTimeout(function(){ $(".loader").fadeOut("slow"); }, 500);
});
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
