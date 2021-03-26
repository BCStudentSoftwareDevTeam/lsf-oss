function getDepartmentPositions(object, stopSelectRefresh="") { // get department from select picker
   var departmentOrg = $(object).val();
   var departmentAcct = $(object).find('option:selected').attr('value-account');
   var url = "/positionDescription/getPositions/" + departmentOrg + "/" + departmentAcct;
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

function clearTerms() {
  // This method will clear both of the term select pickers.
  $("#oldTerm").prop("disabled", false);
  $("#newTerm").prop("disabled", false);
  $("#oldTerm").val('default');
  $("#oldTerm").selectpicker("refresh");
  $("#newTerm").val('default');
  $("#newTerm").selectpicker("refresh");
  CKEDITOR.instances["editor1"].setData('');
}

function fillPositionDescription(termID) {
  // This function will fill the position description for both the
  // previous and current
  CKEDITOR.instances["editor1"].setData('');
  var term = $("#" + termID).val();
  var position = $("#position").val();
  var data = {"positionCode": position, "termCode": term}
  data = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "/positionDescription/getPositionDescription",
    data: data,
    contentType: 'application/json',
    success: function (response){
      var data = response["description"]
      if (termID == "oldTerm") {
        console.log(data)
        $("#pastPositionDescription").html(data);
        console.log("Old term add")
      }
      if (termID == "newTerm") {
        CKEDITOR.instances["editor1"].insertHtml(data);
      }
     }
   });
}

function saveChanges() {
  // This function will save the changes made to the
  // select position description
  if (!$("#newTerm").val()){
    $("#flash_container").html('<div class="alert alert-danger" role="alert" id="flasher">No changes to be saved.</div>');
    $("#flasher").delay(5000).fadeOut();
  }
  else{
    $("#modal").modal("show");
  }
}

function updatePositionDescription() {
  // This function will send the changes to the database
  // in order to update the given positon description.
  var newDescription = CKEDITOR.instances.editor1.getData();
  var positionCode = $("#position").val();
  var term = $("#newTerm").val();
  var data = {"positionDescription": newDescription, "POSN_CODE": positionCode, "termCode": term}
  console.log(data)
  data = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "/positionDescription/updatePositionDescription",
    data: data,
    contentType: 'application/json',
    success: function (response){
      location.reload();
     }
   });
}
