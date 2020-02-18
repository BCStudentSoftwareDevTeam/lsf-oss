$(document).ready(function(){
  fillHoursPerWeek();
   var department = $("#Department").eq(0).val();
   var url = "/modifyLSF/getPendingPosition/" + department;
       $.ajax({
         url: url,
         dataType: "json",
         success: function (response){
            fill_supervisor(response);
            fill_positions(response);
            jobPositionDisable();
         }
       })
 });

$("#contractHoursDiv").hide();
$("#weeklyHoursDiv").hide();
//adds a contstraint that does not allow user to set date before today's date
// var date = new Date();
// date.setDate(date.getDate());
// $("#datetimepicker0").datepicker({
//   minDate: date
// });
// $("#datetimepicker0").datepicker("setDate", "date");
//
// $('.glyphicon-calendar').click(function() {
//     $("#datetimepicker0").focus();
// });

function fill_positions(response) {
  var selected_positions = $("#POSN_TITLE")[0];
    for (var key in response) {
      try{
        var options = document.createElement("option");
        options.text = response[key]["position"].toString() + " " + "(" + response[key]["WLS"].toString() + ")"
        options.value = response[key]["position"].toString() + " " + "(" + response[key]["WLS"].toString() + ")";
        selected_positions.appendChild(options);
      }
      catch(error){
        console.log(error)
      }
    $('.selectpicker').selectpicker('refresh');
  }
}

function fill_supervisor(response){
  var selected_supervisors = $("#supervisor");
    for (var key in response) {
      try{
        var options = document.createElement("option");
        options.text = response[key]["supervisorFirstName"].toString() + " " + response[key]["supervisorLastName"].toString();
        options.value =response[key]["supervisorPIDM"].toString();
        selected_supervisors[0].appendChild(options);
        $('.selectpicker').selectpicker('refresh');
        var map = {};
        $('select option').each(function () {
            if (map[this.value]) {
                $(this).remove()
            }
            map[this.value] = true;
        })
      }
      catch(error){
        console.log(error)
      }
  }
}

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

// function WLScheck(){
//   try{
//     var jobType = $("#jobType").val();
//     var wls = $("#POSN_TITLE").find("option:selected").attr("data-wls");
//   }
//   catch(error){
//     console.log(error)
//   }
// }

// Pops up a modal for overload
// function hourscheck(){
//   var hour = $("#weeklyHours").val();
//   if (hour == "20") {
//       $('#OverloadModal').modal('show');
//       $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
//     }
// };

function fillHoursPerWeek(){ // prefill hours per week select picker)
 var wls = $("#POSN_TITLE option:selected").attr("data-wls"); // FIXME: find another way to get WLS when they change select another position
 var selectedHoursPerWeek = $("#weeklyHours");
 var weeklyHours = $("#weeklyHours option:selected")
 var jobType = $("#jobType").val();
 if (selectedHoursPerWeek){
   $("#weeklyHours").empty();
   var list = ["10", "15", "20"];
   if (jobType == "Secondary") {
     list = ["6","10"] // FIXME: I have put 6 for testing. When I put 5 it doesn't show up in the options
   }
   if(wls>5){
     list = ["15", "20"]
   }
   if( weeklyHours == "20"){ // FIXME: Doesn't work
     $('#OverloadModal').modal('show');
     $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
   }
   $(list).each(function(i,hours) {
     selectedHoursPerWeek.append($("<option />").text(hours));
   });
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
            if (response["Success"]) {
              window.location.href = response["url"]
            }
          }
      })
}
