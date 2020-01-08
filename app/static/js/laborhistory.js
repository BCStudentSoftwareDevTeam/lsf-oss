// $(document).on('click','.accept', function(e){
//      $(".modal-fade").modal("hide");
//      $(".modal-backdrop").remove();
//  });

$('#modal').on('show.bs.modal', function (e) {

    var button = $(e.relatedTarget);
    var modal = $(this);

    // load content from HTML string
    //modal.find('.modal-body').html("Nice modal body baby...");

    // or, load content from value of data-remote url
    modal.find('.modal-body').load(button.data("remote"));

});
function openModal(laborStatusKey) {
  /*
    This function gets a response from the controller function: populateModal() in laborHistory.py.  The response is the data for the modal that pops up
    when the position is clicked.
  */
  // $(".modal-fade").modal("hide");
  // $(".modal-backdrop").remove();
  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/' + laborStatusKey,
    success: function(response) {
      // console.log(response);
      var content = response.toString();
      $("#modal").find(".modal-content").empty().append(content);
      $("#modal").modal("show");
    //   angular.run(function($rootScope) {
    //   $rootScope.$on('$routeChangeStart', destroyTheBackdrop);
    //
    //   function destroyTheBackdrop() {
    //     $('.modal-backdrop').hide();
    //   }
    // });
      $("#modify").attr("href", "/modifyLSF/" + laborStatusKey); // will go to the modifyLSF controller
      $("#rehire").attr("href", "/laborstatusform/" + laborStatusKey); // will go to the lsf controller
      $("#release").attr("href", "/laborReleaseForm/" + laborStatusKey); // will go to labor release form controller
    }
  });
}
// prevent a second click for 2 second.
function preventDoubleClick(id){
  onclick_attr = $("#" + id).attr("onclick");
  $("#" + id).attr("onclick","");
  // console.log("I am clicked")
  // $("#positionTable").off('click'); //disables click event
  // $("#modal").modal("show");
  // setTimeout(function(){
  //   //To re-enable:
  //   $("#positionTable").bind("click",eventhandler);}, 1000);
  setTimeout(function(){
     $("#" + id).attr("onclick",onclick_attr);
   }, 2000);
   return false;
}


  // var clickid = document.getElementById("positionTable")
  // console.log(clickid)
  // $(".modalLink").attr("onclick","");
  // // clickid.onclick = null
  // console.log(clickid)
  // setTimeout(fucntion(){
  //   clickid.onlclick = preventDoubleClick;
  //   $("#modal").modal("show");
  // }, 1000);

  // onclick_attr = $("#" + id).attr("onclick");
  // // onclicks = $(".modalLink").map(function(el) {
  // //   return el.attr("onclick")
  // // });
  //
  // $("#" + id).attr("onclick","");
  // setTimeout(function(){
  //   $("#" + id).attr("onclick",onclick_attr);
  // }, 2000);
  // return false;


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
