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
  console.log(termID)
  var dateType = obj.id.split("_")[0]
  console.log(dateType)
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
        console.log(response)
        if(response)
        stateBtnValue = $("#term_btn_" + termCode).val();
        console.log("Here is the state button Value " + stateBtnValue)
        start = $("#start_" + termCode).val();
        console.log(start)
        end = $("#end_" +termCode).val();
        console.log(end)
        if (start != "" && end != "") {
          $('#term_btn_' + termCode).prop('disabled', false)
          console.log("It worked!!")
        }
        console.log("js success")
      }
    });
}

function termStatus(term) {
  var startID = $("#start_" +term);
  var endID = $("#end_" +term);
  var termBtnID = $("#term_btn_" + term);
  var inactiveBtnID = $("#inactive_btn_" + term);

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

        console.log(termBtnID);
         if ($(termBtnID).hasClass("btn-success")) {
            $(termBtnID).removeClass("btn-success");
            $(termBtnID).addClass("btn-danger");
            $(termBtnID).text("Closed");
            //category = "danger";
            }
          else {
            $(termBtnID).removeClass("btn-danger");
            $(termBtnID).addClass("btn-success");
            $(termBtnID).text("Open");
          //  category = "info";
            }
       }
     }
  })
};
