$(document).ready(function(){
  fillHoursPerWeek();
  jobPositionDisable();
 });

$("#contractHoursDiv").hide();
$("#weeklyHoursDiv").hide();

function jobPositionDisable(){
  var termcode = $("#termCode").eq(0).val();
  var specificTerm = termcode.toString().substr(-2);
  if (specificTerm != 11 && specificTerm != 12 && specificTerm != 00){
    $("#jobType").prop("disabled", true);
    $("#jobType").val("Secondary");
    $("#contractHoursDiv").show();
  }
  else{
    $("#weeklyHoursDiv").show();
  }
}

function fillHoursPerWeek(){ // prefill hours per week select picker
  var defaultValue = $("#oldWeeklyHours").val();
  var selectedHoursPerWeek = $("#weeklyHours");
  var jobType = $("#jobType").val();
  var wls = $("#POSN_TITLE option:selected").attr("data-wls");
  if (selectedHoursPerWeek){
       var list = ["10", "12", "15", "20"];
       if (jobType == "Secondary") {
         list = ["5","10"]
       }
       if(wls>=5){
         list = ["15", "20"]
       }
       $("#weeklyHours").empty();
       $(list).each(function(i,hours) {
         selectedHoursPerWeek.append($("<option />").text(hours).val(hours));
       });
       $("#weeklyHours").val(defaultValue);
       $("#weeklyHours").selectpicker("refresh");
  }
}

function checkWLS20(){
  totalhours = $("#totalHours").val();
  weeklyHours = $("#weeklyHours").val();
  console.log("Current hours", totalhours);
  console.log("New total hours", Number(totalhours) + Number(weeklyHours));
  if(weeklyHours == "20"){
    $('#OverloadModal').modal('show');
    $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
  }
  else if(Number(totalhours) + Number(weeklyHours) > 15) {
    $('#OverloadModal').modal('show');
    $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
  }
}

// var effectiveDate = $("#datetimepicker0").datepicker('getDate');
var finalDict = {};

function checkForChange(){
  var oldSupervisor = $("#prefillsupervisor").val();
  var newSupervisor = $("#supervisor").val();
  var oldPostition = $("#prefillposition").val();
  var newPostition = $("#POSN_TITLE").val();
  var date = $("#datetimepicker0").val();
  var oldNotes = $("#oldNotes").val();
  var newNotes = $("#supervisorNotes").val();
  var oldContractHours = $('#oldContractHours').val();
  var newContractHours = $('#contractHours').val();
  var oldWeeklyHours = $('#oldWeeklyHours').val();
  var newWeeklyHours = $('#weeklyHours').val();

  if(oldSupervisor != newSupervisor){
    finalDict["supervisor"] = {"oldValue": oldSupervisor, "newValue": newSupervisor}
  }
  if(oldPostition != newPostition){
    finalDict["POSN_TITLE"] = {"oldValue": oldPostition, "newValue": newPostition}
  }
  if(oldNotes != newNotes){
    finalDict["supervisorNotes"] = {"oldValue": oldNotes, "newValue": newNotes}
  }
  //FIXME: when only weeklyhours is shows either just send weeklyhours dict or maybe make the contract hours null. and vice versa.
  if(oldContractHours != newContractHours){
    finalDict["contractHours"] = {"oldValue": oldContractHours, "newValue": newContractHours}
  }
  if(oldWeeklyHours != newWeeklyHours){
    finalDict["weeklyHours"] = {"oldValue": oldWeeklyHours, "newValue": newWeeklyHours}
  }
  if (JSON.stringify(finalDict) !== '{}'){
    $('#submitModal').modal('show');
    return finalDict
  }
  if (JSON.stringify(finalDict) == '{}'){
    $('#NochangeModal').modal('show');
  }
}

function buttonListener(laborStatusKey) {
  var url = "/modifyLSF/updateLSF/" + laborStatusKey;
  modifiedDict = JSON.stringify(finalDict)
      $.ajax({
        url: url,
        method: "POST",
        contentType: 'application/json',
        data: modifiedDict,
        success: function(response) {
              setTimeout(function() { // executed after 1 second
                 window.location.replace("/laborstatusform"); // reloads the page if every form
               }, 5000);
              // console.log("After success");
              // console.log(response["url"]);
              // window.location.href = response["url"];
              // window.location.replace(response["url"]);
          }
      })
}
