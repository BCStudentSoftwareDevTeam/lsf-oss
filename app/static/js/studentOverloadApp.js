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
  var primaryHours = $("#primaryHours");
  if (primaryHours){
   $("#primaryHours").empty();
   for (var key in response) {
     var input = document.createElement("input");
     input.text = response[key]["primaryHour"].toString();
     input.id = key;
     input.value = key;
     primaryHours.appendChild(input);
   }
  }
 }
