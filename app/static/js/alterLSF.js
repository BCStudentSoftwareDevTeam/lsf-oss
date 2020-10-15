$(document).ready(function(){
  fillHoursPerWeek();
  jobPositionDisable();
 });

$("#contractHoursDiv").hide();
$("#weeklyHoursDiv").hide();
//adds a contstraint that does not allow user to set date before today's date
var date = new Date();
date.setDate(date.getDate());
$("#datetimepicker0").datepicker({
  minDate: date
});
$("#datetimepicker0").datepicker("setDate", "date");

$(".glyphicon-calendar").click(function() {
    $("#datetimepicker0").focus();
});

function jobPositionDisable(){
  var isBreak = $("#termBreak").data("termbreak");
  if (isBreak){
    $("#jobType").prop("disabled", true);
    $("#jobType").val("Secondary");
    $("#contractHoursDiv").show();
    $("#weeklyHours").val("");
  }
  else{
    $("#weeklyHoursDiv").show();
    $("#contractHours").val("");
  }
}

function fillHoursPerWeek(){ // prefill hours per week select picker
  var defaultValue = $("#oldWeeklyHours").val();
  var selectedHoursPerWeek = $("#weeklyHours");
  var jobType = $("#jobType").val();
  var wls = $("#position option:selected").attr("data-wls");
  if (selectedHoursPerWeek){
    var list = ["10", "12", "15", "20"];
    if (jobType == "Secondary") {
      list = ["5","10"]
    }
    if(wls >= 5) {
      list = ["15", "20"]
      // Here we need to pop open the modal that says they need atleast 15 hours
    }
    $("#weeklyHours").empty();
    $(list).each(function(i,hours) {
      selectedHoursPerWeek.append($("<option />").text(hours).val(hours));
    });
    if (wls >= 5){
      if (Number(defaultValue) >= 15){
        $("#weeklyHours").val(defaultValue);
        $("#weeklyHours").selectpicker("render");
        $("#weeklyHours").selectpicker("refresh");
      } else {
        $("#weeklyHours").val('15');
        $("#weeklyHours").selectpicker("render");
        $("#weeklyHours").selectpicker("refresh");
        $("#warningModalTitle").html("Work-Learning-Service Levels (WLS)");
        $("#warningModalText").html("Student with WLS Level 5 or 6 must have at least a 15 hour contract. " +
                                 "These positions require special authorization as specified at " +
                                 "<a href=\"http://catalog.berea.edu/2014-2015/Tools/Work-Learning-Service-Levels-WLS\""+
                                 "target=\"_blank\">The Labor Program Website.</a>");
        $("#warningModalButton").css('display', 'none');
        $("#resetConfirmButton").css('display', 'none');
        $("#warningModal").modal("show");
      }
    } else {
        $("#weeklyHours").val(defaultValue);
        $("#weeklyHours").selectpicker("render");
        $("#weeklyHours").selectpicker("refresh");
    }
    $("#weeklyHours").selectpicker("refresh");
  }
}

var effectiveDate = $("#datetimepicker0").datepicker("getDate");
var finalDict = {};

function checkWLS20(){
  totalhours = $("#totalHours").val();
  weeklyHours = $("#weeklyHours").val();
  if(weeklyHours == "20"){
    $("#OverloadModal").modal("show");
    $("#overloadModalButton").attr("data-target", "") // prevent a Primary Modal from showing up
  }
  else if(Number(totalhours) + Number(weeklyHours) > 15) {
    $("#OverloadModal").modal("show");
    $("#overloadModalButton").attr("data-target", "") // prevent a Primary Modal from showing up
  }
}

function checkSupervisor() {
  var oldSupervisor = $('#prefillsupervisor').val();
  var supervisor = $('#supervisor').val()
  var position = $('#position').val()
  var oldPostition = $('#prefillposition').val()
  var weeklyHours = $('#weeklyHours').val()
  var oldWeeklyHours = $('#oldWeeklyHours').val()
  var contractHours = $('#contractHours').val()
  var oldContractHours = $('#oldContractHours').val()

  if (supervisor != oldSupervisor) {
    $('#position').val(oldPostition);
    $("#position").prop('disabled', true);
    $('#position').selectpicker('refresh');
    $('#weeklyHours').val(oldWeeklyHours);
    $("#weeklyHours").prop('disabled', true);
    $('#weeklyHours').selectpicker('refresh');
    $('#contractHours').val(oldContractHours);
    $("#contractHours").prop('disabled', true);
    $('#contractHours').selectpicker('refresh');
    category = "info"
    msg = "Changes to Hours and Position are unavailable when Supervisor is changed. (Select Original Supervisor to change Position or Hours)";
    $("#flash_container").html('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
    $("#flasher").delay(3000).fadeOut()
  } else {
    $("#position").prop('disabled', false)
    $('#position').selectpicker('refresh');
    $("#weeklyHours").prop('disabled', false);
    $('#weeklyHours').selectpicker('refresh');
    $("#contractHours").prop('disabled', false);
    $('#contractHours').selectpicker('refresh');
  }
}

function checkForChange(){
  var oldSupervisor = $("#prefillsupervisor").val();
  var newSupervisor = $("#supervisor").val();
  var oldPostition = $("#prefillposition").val();
  var newPosition = $("#position").val();
  var date = $("#datetimepicker0").val();
  var oldNotes = $("#oldNotes").val();
  var newNotes = $("#supervisorNotes").val();
  var oldContractHours = $("#oldContractHours").val();
  var newContractHours = $("#contractHours").val();
  var oldWeeklyHours = $("#oldWeeklyHours").val();
  var newWeeklyHours = $("#weeklyHours").val();

  if(oldSupervisor != newSupervisor){
    finalDict["supervisor"] = {"oldValue": oldSupervisor, "newValue": newSupervisor, "date": date}
  }
  if(oldPostition != newPosition){
    finalDict["position"] = {"oldValue": oldPostition, "newValue": newPosition, "date": date}
  }
  if(oldNotes != newNotes){
    finalDict["supervisorNotes"] = {"oldValue": oldNotes, "newValue": newNotes, "date": date}
  }
  if(oldContractHours != newContractHours && newWeeklyHours == ""){
    finalDict["contractHours"] = {"oldValue": oldContractHours, "newValue": newContractHours, "date": date}
  }
  if(oldWeeklyHours != newWeeklyHours && newContractHours == ""){
    finalDict["weeklyHours"] = {"oldValue": oldWeeklyHours, "newValue": newWeeklyHours, "date": date}
  }

  if (JSON.stringify(finalDict) == "{}" || (Object.keys(finalDict).length == 1 && Object.keys(finalDict) == "supervisorNotes")){
    $("#NochangeModal").modal("show");
  }
  else if (newNotes == '') {
    category = "danger"
    msg = "Please make sure Notes is filled out.";
    $("#flash_container").html('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
    $("#flasher").delay(3000).fadeOut()
  }
  else if (JSON.stringify(finalDict) !== "{}"){
    $("#submitModal").modal("show");
    return finalDict
  }

}

function buttonListener(laborStatusKey) {
  event.preventDefault();
  $('#modal').html('Processing');
  $('#modal').prop('disabled', 'True');
  $('#adjustmentClose').prop('disabled', 'True');
  $.ajax({
    url: "/alterLSF/submitAlteredLSF/" + laborStatusKey,
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify(finalDict),
    success: function(response) {
      window.location.href = document.referrer;
    }
  })
}
