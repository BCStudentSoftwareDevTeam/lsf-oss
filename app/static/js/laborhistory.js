function hello(laborStatusKey) {
  console.log(laborStatusKey);
  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/' + laborStatusKey,
    //data: JSON.stringify({"laborStatusFormID": laborStatusKey}),
    success: function(response) {
      $("#holdModal").empty().append(response);
      $("#modal").modal("show");
    }
  });

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
