function getDepartmentPositions(object, stopSelectRefresh="") { // get department from select picker
   var departmentOrg = $(object).val();
   var departmentAcct = $(object).find('option:selected').attr('value-account');
   var url = "/positionDescriptions/getPositions/" + departmentOrg + "/" + departmentAcct;
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

function updateVersion(positionID) {
  // This method will clear both of the term select pickers.
  $("#preVersion").prop("disabled", false);
  $("#preVersion").empty();
  $("#preVersion").selectpicker("refresh");
  $("#pastPositionDescription").html("");
  console.log("Cleared the SP")
  console.log(positionID)
  var data = {"POSN_CODE": positionID}
  data = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "/positionDescriptions/getVersions",
    data: data,
    contentType: 'application/json',
    success: function (response){
      var versionCount = 1
      for (var key in response) {
       if (response[key].endDate == "None") {
         var versionStatus = "(Current Version)"
       }
       else {
         var versionStatus = "(" + response[key].createdDate + " - " + response[key].endDate + ")"
       }
       $("#preVersion").append(
         $("<option />")
            .attr("data-content", "<span> Version " + versionCount
            + "</span>" + "<small class='text-muted'>" + " " + versionStatus + "</small>")
            .attr("id", key)
            .attr("value", key)
       );
       versionCount += 1
      }
      $("#preVersion").selectpicker("refresh");
     }
   });
}

function fillPositionDescription(versionID) {
  // This function will fill the position description for both the
  // previous and current
  // CKEDITOR.instances["editor1"].setData('');
  var versionID = $("#preVersion").val();
  console.log(versionID)


  console.log(versionID)
  var data = {"positionDescriptionID": versionID}
  data = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "/positionDescriptions/getPositionDescription",
    data: data,
    contentType: 'application/json',
    success: function (response){
      // Need to put all of the text into the textarea now
      console.log("Made it back here");
      console.log(response);
      $("#pastPositionDescription").html(response);
     }
   });
}

function saveChanges() {
  // This function will save the changes made to the
  // select position description
  if (!$("#preVersion").val()){
    $("#flash_container").html('<div class="alert alert-danger" role="alert" id="flasher">No version has been selected.</div>');
    $("#flasher").delay(5000).fadeOut();
  }
  else{
    $("#modal").modal("show");
  }
}

function beginEdit() {
  // This function will send the changes to the database
  // in order to update the given positon description.
  var versionID = $("#preVersion").val();
  console.log(versionID)
  window.location.href = '/positionDescriptionEdit/' + versionID

}
