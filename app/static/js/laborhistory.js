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

document.getElementById("current").addEventListener("click",function(){
  console.log("Here")
  $(currentStu).show();
  $(pastStu).hide();
  $(".pastStu").attr("disabled", true)
  $(".actStu").removeAttr("disabled")
}, false);
document.getElementById("past").addEventListener("click",function(){
  console.log("Here")
  $(currentStu).hide();
  $(pastStu).show();
  $(".actStu").attr("disabled", true)
  $(".pastStu").removeAttr("disabled")
}, false);
document.getElementById("all").addEventListener("click",function(){
  console.log("Here")
  $(currentStu).show();
  $(pastStu).show();
  $(".pastStu").removeAttr("disabled")
  $(".actStu").removeAttr("disabled")
}, false);

$('.openBtn').on('click',function(){
    $('.modal-body').load('index.html',function(){
        $('#laborHistoryDownloadModal').modal({show:true});
    });

});

$('#select-all').click(function(event) {
  console.log("Here")
    if(this.checked) {
        // Iterate each checkbox
        $(':checkbox').not("[disabled]").each(function() {
            this.checked = true;
        });
    } else {
        $(':checkbox').not("[disabled]").each(function() {
            this.checked = false;
        });
    }
});

function downloadHistory(){
  $('input[type="checkbox"]:checked').prop('checked',false);

}

function withdrawform(formID){
  console.log(formID)
  formid_dict={}
  formid_dict["FormID"] = formID
  console.log(formid_dict)
  data = JSON.stringify(formid_dict);
  $.ajax({
         method: "POST",
         url: '/laborHistory/modal/updatestatus',
         data: data,
         contentType: 'application/json',
         success: function(response) {
             if (response["Success"]) {
               msg = "Withdraw Happened";
               category = "danger";
               $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>');
               $("#flasher").delay(4000).fadeOut();
               return;
             }
           }
         });
       }
