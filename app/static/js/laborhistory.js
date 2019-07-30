function openModal(laborStatusKey) {
  console.log(laborStatusKey);
  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/' + laborStatusKey,
    //data: JSON.stringify({"laborStatusFormID": laborStatusKey}),
    success: function(response) {
      console.log(response);
      $("#holdModal").empty().append(response);
      $("#modal").modal("show");
      console.log(laborStatusKey)
      $("#rehire").href="/laborstatusform/" + laborStatusKey;
    }
  });

}

function redirectLaborStatusForm() {
  window.location.href = "/laborstatusform"
}

function redirectModifiedLaborForm() {
  window.location.href = "/"
}

function redirectLaborReleaseForm() {

}

function redirectModifiedPendingForm() {

}

function withdrawOverloadForm() {

}

// function hello(laborStatusKey) {
//
//   $.ajax({
//     type: "GET",
//     url: '/laborHistory/modal/' + laborStatusKey,
//     //data: JSON.stringify({"laborStatusFormID": laborStatusKey}),
//     success: function(modalDictionary) {
//       var modalData = JSON.parse(modalDictionary)
//       console.log(modalData);
//       $("p").html(modalData["studentName"])
//       $("#holdModal").append(response)
//       $("#modal").modal("show");
//     }
//   });
//
// }
