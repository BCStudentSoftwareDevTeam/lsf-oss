$('.datepicker').datepicker()
   .on('changeDate', function(e) {
     alert($(this).data('startEnd'));
     console.log($(this).data('startEnd'));
   });

$('.glyphicon-calendar').click(function() {
   $(".datepicker").focus();
 });

var date = new Date();
date.setDate(date.getDate());
$(".form-control").datepicker({
});


function getDate(obj, termCode) {

  var termStart = obj.value; // This is the start date
  var termID = obj.id.split("_")[1] //
  var dateType = obj.id.split("_")[0]
  var tabledata_dict = {};
  tabledata_dict[dateType] = obj.value;
  tabledata_dict["termCode"] = termID;
  data = JSON.stringify(tabledata_dict);
  console.log(data)
    $.ajax({
      type: "POST",
      url: "/termManagement/setDate/",
      datatype: "json",
      data: data,
      contentType: 'application/json',
      success: function(response){
        console.log("js success")
      }
    });
}

function termStatus(term) {
  console.log(term)
    $.ajax({
      method: "POST",
      url: "/termManagement/manageStatus ",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({"termBtn": term}),
      processData: false,
      success: function(response) {
      console.log(response);
      if(response["Success"]) {
        //category = "info"
        console.log("Hello, this works")
        var termBtnID = $("#term_btn_" + term);
        console.log(termBtnID);
         if ($(termBtnID).hasClass("btn-success")) {
            $(termBtnID).removeClass("btn-success");
            $(termBtnID).addClass("btn-danger");
            $(termBtnID).text("Open");
            //category = "danger";
            }
          else {
            $(termBtnID).removeClass("btn-danger");
            $(termBtnID).addClass("btn-success");
            $(termBtnID).text("Closed");
          //  category = "info";
            }
       }
     }
  })
};
