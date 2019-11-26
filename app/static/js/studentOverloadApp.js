function getCurrentPrimary(object) { // get current primary position from select picker
  var primary = $("#Primary").val();
  var url = "/studentOverloadApp/getPrimary/" + primary;
     $.ajax({
       url: url,
       dataType: "json",
       success: function (response){
          fillPrimaryHour(response)
       }
     })
 }

function fillPrimaryHour(response){ // HAVE ERRORS
  $("#primaryHours").attr("value", '');
  for (var key in response) {
    console.log("here2")
    $("#primaryHours").attr("type", "text");
    $("#primaryHours").attr("value", response[key]["primaryHour"]);
   }
 }
