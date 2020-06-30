$(document).ready(function(){
  fillHoursPerWeek();
  jobPositionDisable();
 });

$("#contractHoursDiv").hide();
$("#weeklyHoursDiv").hide();

function jobPositionDisable(){
  var isBreak = $("#termBreak").data('termbreak');
  if (isBreak){
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
  var wls = $("#Position option:selected").attr("data-wls");
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

var finalDict = {};

function checkWLS20(){
  totalhours = $("#totalHours").val();
  weeklyHours = $("#weeklyHours").val();
  if(weeklyHours == "20"){
    $('#OverloadModal').modal('show');
    $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
  }
  else if(Number(totalhours) + Number(weeklyHours) > 15) {
    $('#OverloadModal').modal('show');
    $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
  }
}

function checkForChange(){
  var oldSupervisor = $("#prefillsupervisor").val();
  var newSupervisor = $("#supervisor").val();
  var oldPostition = $("#prefillposition").val();
  var newPostition = $("#Position").val();
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
    finalDict["position"] = {"oldValue": oldPostition, "newValue": newPostition}
  }
  if(oldNotes != newNotes){
    finalDict["supervisorNotes"] = {"oldValue": oldNotes, "newValue": newNotes}
  }
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
  $.ajax({
    url: "/alterLSF/updateLSF/" + laborStatusKey,
    method: "POST",
    contentType: 'application/json',
    data: JSON.stringify(finalDict),
    success: function(response) {
      window.location.href = document.referrer;
    }
  })
}
