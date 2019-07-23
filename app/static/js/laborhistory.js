function hello(laborStatusKey) {
  console.log(laborStatusKey)

  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/' + laborStatusKey,
    //data: JSON.stringify({"laborStatusFormID": laborStatusKey}),
    success: function(request) {
      $("#modal").modal("show");
    }
  });


  //$("#modal").modal("show");

}
