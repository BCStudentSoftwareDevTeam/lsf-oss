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

function fillPrimaryHour(response){
  if ($("#primaryHours").val() != ''){
    $("#primaryHours").val("");
  }
  for (var key in response){
    $("#primaryHours").attr("type", "text");
    $("#primaryHours").val(response[key]["primaryHour"]);
    $("#primaryHours").attr("text", response[key]["primaryHour"]);
  }
  updateSum()
}

function getCurrentSecondary(object) { // get current secondary position from select picker
  var secondary = $("#Secondary").val();
  var url = "/studentOverloadApp/getSecondary/" + secondary;
     $.ajax({
       url: url,
       dataType: "json",
       success: function (response){
          fillSecondaryHour(response)
       }
     })
 }

function fillSecondaryHour(response){
  if ($("#secondaryHours").val() != ''){
    $("#secondaryHours").val("");
  }
  for (var key in response){
    $("#secondaryHours").attr("type", "text");
    $("#secondaryHours").val(response[key]["secondaryHour"]);
    $("#secondaryHours").attr("text", response[key]["secondaryHour"]);
  }
  updateSum()
}

function updateSum(){
  var primaryHours = (isNaN(parseInt($("#primaryHours").val()))) ? 0 : parseInt($("#primaryHours").val());
  var secondaryHours = (isNaN(parseInt($("#secondaryHours").val()))) ? 0 : parseInt($("#secondaryHours").val());
  var overloadHours = (isNaN(parseInt($("#overloadHours").val()))) ? 0 : parseInt($("#overloadHours").val());
  $("#currentTotal").val(primaryHours + secondaryHours)
  $("#overloadTotal").val(primaryHours + secondaryHours + overloadHours)
  console.log(primaryHours)
  console.log(secondaryHours)
}

function checkForEmptyFields(){
  console.log("here2")
  console.log($("#notes").val())
  if($("#Primary").val() != null && $("#notes").val() != "") {
    console.log("here1")
    $('#submitModal').modal('show');
  }
}
