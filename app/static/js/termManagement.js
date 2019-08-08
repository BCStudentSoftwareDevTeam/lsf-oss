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

$(document).ready(function () {
  $(".start").datepicker({
      dateFormat: "M-dd-yy",
      minDate: 0,
      onSelect: function (date) {
          var date2 = $('.end').datepicker('getDate');
          date2.setDate(date2.getDate() + 1);
          $('.start').datepicker('setDate', date2);
          //sets minDate to dt1 date + 1
          $('.start').datepicker('option', 'minDate', date2);
      }
  });
  $('.start').datepicker({
      dateFormat: "M-dd-yy",
      onClose: function () {
          var dt1 = $('.start').datepicker('getDate');
          console.log(dt1);
          var dt2 = $('.end').datepicker('getDate');
          if (dt2 <= dt1) {
              var minDate = $('#dt2').datepicker('option', 'minDate');
              $('.end').datepicker('setDate', minDate);
          }
      }
  });
});

// function DateCheck()
// {
//   var StartDate= document.getElementById('start_201700').value;
//   var EndDate= document.getElementById('end_201700').value;
//   var eDate = new Date(EndDate);
//   var sDate = new Date(StartDate);
//   if(StartDate!= '' && StartDate!= '' && sDate> eDate)
//     {
//     alert("Please ensure that the End Date is greater than or equal to the Start Date.");
//     return false;
//     }
// }

// function {
//   $("#start_201700").datepicker({
//       onClose: function(selected) {
//         var dt = new Date(selected);
//         dt.setDate(dt.getDate() + 1);
//         $("#end_201700").datepicker("option","minDate", dt);
//       }
//   });
//   // $("#end_201700").datepicker({
  //     onClose: function(selected) {
  //       var dt = new Date(selected);
  //       dt.setDate(dt.getDate() - 1);
  //       $("#start_201700").datepicker("option","maxDate", dt);
  //     }
  // });
// }

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
        start = $("#start_" + termCode).val();
        console.log(start)
        end = $("#end_" +termCode).val();
        console.log(end)
        if (start != "" && end != "") {
          $('#term_btn_' + termCode).prop('disabled', false)
          console.log("It worked!!")
        }
    //     $("#start_" + termCode).datepicker({
    //     onClose: function(selected) {
    //       console.log($("#end_" + termCode), $("#start_" + termCode));
    //       console.log("hello")
    //         $("#end_" + termCode).datepicker("option", "minDate", selected);
    //     }
    // });
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
