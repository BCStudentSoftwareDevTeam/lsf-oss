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
  if(weeklyHours == "20"){
    $('#OverloadModal').modal('show');
    $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
  }
  else if(Number(totalhours) + Number(weeklyHours) > 15) {
    $('#OverloadModal').modal('show');
    $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
  }
}

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

function buttonListener(laborStatusKey, cookie) {
  $.ajax({
    url: "/modifyLSF/updateLSF/" + laborStatusKey + "/" + cookie,
    method: "POST",
    contentType: 'application/json',
    data: JSON.stringify(finalDict),
    success: function(response) {
      window.location.href = response["url"];
    }
  })
}

function getCookie(){
  // Get the cookie if it was created
  var name = "pageClicked" + "=";
  if(document.cookie == name + "pendingForms"){
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);}
      if (c.indexOf(name) == 0) {
        var cookieValue = c.substring(name.length, c.length);  // get cookie value specified under cookie name
        document.cookie = "pageClicked=; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/"; // deletes the cookie by setting expiration to a past date
        return cookieValue;
      }
    }}
  return "notPendingForms";
}
