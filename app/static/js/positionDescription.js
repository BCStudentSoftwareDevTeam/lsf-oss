$("#warningTitle").hide()

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
  var data = {"POSN_CODE": positionID}
  data = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "/positionDescriptions/getVersions",
    data: data,
    contentType: 'application/json',
    success: function (response){

      if (Object.keys(response).length == 0) {
        $("#newVersionFooter").html('<button type="button" class="btn btn-danger" data-dismiss="modal" style="float:left">Close</button>' +
                                    '<button type="button" class="btn btn-success" value=' + positionID + ' onclick="beginNewVersionEdit(this.value)" style="float:right">Create</button>')
        $("#newVersion").modal("show");
      }


      var versionCount = 1
      var disableButton = false
      for (var key in response) {
        if (response[key].status == "Approved") {
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
        else if (response[key].status == "Pending") {
          disableButton = true
        }
      }
      $("#preVersion").selectpicker("refresh");
      if (disableButton == false) {
        $("#editButton").prop('disabled', false)
        $("#warningTitle").hide()
      }
      else if (disableButton == true) {
        $("#editButton").prop('disabled', true)
        $("#warningTitle").show()
      }
    }
   });
}

function checkDescription(positionID){
  var data = {"POSN_CODE": positionID}
  data = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "/positionDescriptions/checkDescription",
    data: data,
    contentType: 'application/json',
    success: function (response){
      console.log("getting back", response);
    }
  });
}

function fillPositionDescription(versionID) {
  // This function will fill the position description for both the
  // previous and current
  // CKEDITOR.instances["editor1"].setData('');
  var versionID = $("#preVersion").val();
  var data = {"positionDescriptionID": versionID}
  data = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "/positionDescriptions/getPositionDescription",
    data: data,
    contentType: 'application/json',
    success: function (response){
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
  window.location.href = '/positionDescriptionEdit/' + versionID

}

function beginNewVersionEdit(positionCode) {
  // This function will redirect the user to the position
  // description edit page when creating the first version of a
  // position description.
  console.log("Redirect")
  window.location.href = '/positionDescriptionEdit/newVersion/' + positionCode
}
