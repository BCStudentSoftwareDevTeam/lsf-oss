$("#contractHoursDiv").hide();
$("#weeklyHoursDiv").hide();
//adds a contstraint that does not allow user to set date before today's date
var date = new Date();
date.setDate(date.getDate());
$("#datetimepicker0").datepicker({
  minDate: date
});
$("#datetimepicker0").datepicker("setDate", "date");

$('.glyphicon-calendar').click(function() {
    $("#datetimepicker0").focus();
});

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

$(document).ready(function(){
   var department = $("#Department").eq(0).val();
   var url = "/modifyLSF/getPosition/" + department;
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

function jobPositionDisable(){
  var termcode = $("#termCode").eq(0).val();
  var specificTerm = termcode.toString().substr(-2);
  if (specificTerm != 11 && specificTerm != 12 && specificTerm != 00){
    $("#jobType")[0].prop("disabled", true);
    $("#jobType").val("Secondary");
      WLScheck()
      $("#contractHoursDiv").show();
  }
  else{
    $("#weeklyHoursDiv").show();
  }
}

function WLScheck(){
  try{
    var jobType = $("#jobType").val();
    var selected = []
    $("#POSN_TITLE option").each(function()
    {
    selected.push($(this).val().substr(-3))
    });
    var wls5 = selected.indexOf('(5)')
    var wls6 = selected.indexOf('(6)')
    if (jobType == "Secondary"){
      var selectedPosition = $('#POSN_TITLE option:selected').val().substr(-3)
      if((wls6 >= 0 || wls5 >= 0) && (selectedPosition == "(6)" || selectedPosition =="(5)")){
        $('#POSN_TITLE option').eq(wls6).prop('disabled', true);
        $('#POSN_TITLE option').eq(wls5).prop('disabled', true);
        $("#POSN_TITLE").val(1);
        $('.selectpicker').selectpicker('refresh');
      }
      if((selectedPosition != "(6)" || selectedPosition !="(5)") && (wls6 >= 0 || wls5 >= 0)){
        $('#POSN_TITLE option').eq(wls6).prop('disabled', true);
        $('#POSN_TITLE option').eq(wls5).prop('disabled', true);
        $('.selectpicker').selectpicker('refresh');
      }
    }
    if (jobType == "Primary"){
      if(wls6 >= 0 || wls5 >= 0){
        $('#POSN_TITLE option').eq(wls6).prop('disabled', false);
        $('#POSN_TITLE option').eq(wls5).prop('disabled', false);
        $('.selectpicker').selectpicker('refresh');
      }
      else{
        $('#POSN_TITLE option').eq(wls6).prop('disabled', true);
        $('#POSN_TITLE option').eq(wls5).prop('disabled', true);
        $('.selectpicker').selectpicker('refresh');
      }
    }
  }
  catch(error){
    console.log(error)
  }
}

// Pops up a modal for overload
function hourscheck(){
  var hour = $("#weeklyHours")[0].val();
  if (hour == "20") {
      $('#OverloadModal').modal('show');
      $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
    }
};

function fillHoursPerWeek(fillhours=""){ // prefill hours per week select picker)
 var selectedHoursPerWeek = $("#weeklyHours")[0];
 var jobType = $("#jobType").val();
 if (selectedHoursPerWeek){
   $("#weeklyHours").empty();
   if (jobType == "Primary"){
     var options = document.createElement("option");
     var dict = {
       10: "10",
       12: "12",
       15: "15",
       20: "20"}
     for (var key in dict){
       selectedHoursPerWeek.options[selectedHoursPerWeek.options.length]= new Option(dict[key], key);
     }
   }
   else if (jobType == "Secondary") {
     var options = document.createElement("option");
     var dict = {
       5: "5",
       10: "10"}
     for (var key in dict){
       selectedHoursPerWeek.options[selectedHoursPerWeek.options.length]= new Option(dict[key], key);
     }
   }
   if (fillhours == ""){
     $('.selectpicker').selectpicker('refresh');
   }
 }
}

var effectiveDate = $("#datetimepicker0").datepicker('getDate');
var finalDict = {};

function checkForChange(){
  var oldSupervisor = $("#prefillsupervisor").val();
  var newSupervisor = $("#supervisor").val();
  var oldPostition = $("#prefillposition").val();
  var newPostition = $("#POSN_TITLE").val();
  var date = $("#datetimepicker0").val();
  var oldNotes = $("#oldNotes").val();
  var newNotes = $("#supervisorNotes").val();

  if(oldSupervisor != newSupervisor){
    finalDict["supervisor"] = {"oldValue": oldSupervisor, "newValue": newSupervisor, "date": date}
  }
  if(oldPostition != newPostition){
    finalDict["POSN_TITLE"] = {"oldValue": oldPostition, "newValue": newPostition, "date": date}
  }
  if(oldNotes != newNotes){
    finalDict["supervisorNotes"] = {"oldValue": oldNotes, "newValue": newNotes, "date": date}
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
  var url = "/modifyLSF/submitModifiedForm/" + laborStatusKey;
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
