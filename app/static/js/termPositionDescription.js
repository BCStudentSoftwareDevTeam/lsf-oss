function getDepartmentPositions(object, stopSelectRefresh="") { // get department from select picker
   var departmentOrg = $(object).val();
   var departmentAcct = $(object).find('option:selected').attr('value-account');
   var url = "/termPositionDescription/getPositions/" + departmentOrg + "/" + departmentAcct;
       $.ajax({
         url: url,
         dataType: "json",
         success: function (response){

           fillPositions(response, stopSelectRefresh);
          }
        });
  }

function fillPositions(response, stopSelectRefresh="") { // prefill Position select picker with the positions of the selected department
  var selectedPositions = $("#position");
  $("#position").empty();
  $("#position").prop("disabled", false);
  for (var key in response) {
    console.log(key);
   selectedPositions.append(
     $("<option />")
        .attr("data-content", "<span>" + response[key].position + " " + "(" + response[key].WLS+ ")"
        + "</span>" + "<small class='text-muted'>" + " " + "(" + response[key].positionCode + ")" + "</small>")
        .attr("id", key)
        .attr("value", key)
        .attr("data-wls", response[key].WLS)
   );

  }
  if (stopSelectRefresh== "") {
   $(".selectpicker").selectpicker("refresh");
  }
  else {
   value = $("#position").val();
   $("#position").val(value);
  }
}

function fillPositionDescription(termID) {
  // This function will fill the position description for both the
  // previous and current
  var term = $("#" + termID).val();
  var position = $("#position").val();
  console.log("Term", term);
  console.log("Position", position);
  var data = {"positionCode": position, "termCode": term}
  data = JSON.stringify(data);
  console.log(data);
  $.ajax({
    type: "POST",
    url: "/termPositionDescription/getPositionDescription",
    data: data,
    contentType: 'application/json',
    success: function (response){
      console.log("Made it back to the JS");
     }
   });
}
