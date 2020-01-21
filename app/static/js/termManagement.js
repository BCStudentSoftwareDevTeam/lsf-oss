$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

$('.glyphicon-calendar').click(function() {  // gets the calender glyphicon
   $(".datepicker").focus();
 });

var date = new Date();
date.setDate(date.getDate());
$(".form-control").datepicker({
});

function getDate(obj, termCode) {
  /* this function makes a dictionary with term code being the keys, and the dates being the values
  then this will trigger the ajax call and send the dictionary to termManagement.py */
  var termStart = obj.value; // You need to get the value of this object otherwise it will show "object Object"
  var termID = obj.id.split("_")[1] // This is how we format the term code
  var dateType = obj.id.split("_")[0] // This variable stores whether the value is a start date or an end date
  var tabledata_dict = {};
  tabledata_dict[dateType] = obj.value;
  tabledata_dict["termCode"] = termID;
  data = JSON.stringify(tabledata_dict); // need to do this in order for the python to recognize it
    $.ajax({
      type: "POST",
      url: "/termManagement/setDate/",
      datatype: "json",
      data: data,
      contentType: 'application/json',
      success: function(response){

        if(response)
        stateBtnValue = $("#term_btn_" + termCode).val();
        start = $("#start_" + termCode).val();
        end = $("#end_" +termCode).val();

        if (start != "" && end != "") {
          $('#term_btn_' + termCode).prop('disabled', false)
        }
      }

    });
}

function updateStart(obj, termCode){
  /* This function disables any dates that come after the selected end date */
  var newEnd = new Date(obj.value)
  var dayNewEnd = newEnd.getDate() - 1;
  var monthNewEnd = newEnd.getMonth();
  var yearNewEnd = newEnd.getFullYear();
  $('#start_' + termCode).datepicker({maxDate: new Date(yearNewEnd, monthNewEnd, dayNewEnd)});
  $('#start_' + termCode).datepicker( "option", "maxDate", new Date(yearNewEnd, monthNewEnd, dayNewEnd));
}

function updateEnd(obj, termCode){
  /* This function disables any dates that come after the selected start date */
  var newStart = new Date(obj.value)
  var dayNewStart = newStart.getDate() + 1;
  var monthNewStart = newStart.getMonth();
  var yearNewStart = newStart.getFullYear();
  $('#end_' + termCode).datepicker({minDate: new Date(yearNewStart, monthNewStart, dayNewStart)});
  $("#end_" + termCode).datepicker( "option", "minDate", new Date(yearNewStart, monthNewStart, dayNewStart));
}

function termStatus(term) {
  /* this function changes the buttons from close and open whenever they are clicked */
  var startID = $("#start_" + term); // This is how we get the unique ID, term is the term code
  var endID = $("#end_" + term);
  var termBtnID = $("#term_btn_" + term);
  var inactiveBtnID = $("#inactive_btn_" + term);
    $.ajax({
      method: "POST",
      url: "/termManagement/manageStatus ",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({"termBtn": term}),
      processData: false,
      success: function(response) {
      if(response["Success"]) {
        //category = "info"
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
