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
$(document).ready(function(){
  var map = {};
  $('select option').each(function () {
      if (map[this.value]) {
          $(this).remove()
      }
      map[this.value] = true;
  })
});
function fill_positions(response) {
  var selected_positions = document.getElementById("POSN_TITLE");
    for (var key in response) {
      var options = document.createElement("option");
      options.text = response[key]["position"].toString() + " " + "(" + response[key]["WLS"].toString() + ")"
      options.value = response[key]["position"].toString() + " " + "(" + response[key]["WLS"].toString() + ")";
      selected_positions.appendChild(options);
    $('.selectpicker').selectpicker('refresh');
  }
}
function fill_supervisor(response){
  var selected_supervisors = document.getElementById("supervisor");
    for (var key in response) {
      var options = document.createElement("option");
      options.text = response[key]["supervisorFirstName"].toString() + " " + response[key]["supervisorLastName"].toString();
      options.value = response[key]["supervisorPIDM"].toString();
      selected_supervisors.appendChild(options);
    $('.selectpicker').selectpicker('refresh');
  }
}
$(document).ready(function(){
   var department = document.getElementById("Department").value;
   var url = "/modifyLSF/getPosition/" + department;
       $.ajax({
         url: url,
         dataType: "json",
         success: function (response){
            fill_positions(response);
            fill_supervisor(response);
            jobPositionDisable();
         }
       })
 });
function jobPositionDisable(){
  var termcode = document.getElementById("termCode").value;
  var specificTerm = termcode.toString().substr(-2);
  if (specificTerm != 11 && specificTerm != 12 && specificTerm != 00){
    document.getElementById("jobType").disabled = true;
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
    console.log(selectedPosition)
    var wls5 = selected.indexOf('(5)')
    var wls6 = selected.indexOf('(6)')
    if (jobType == "Secondary"){
      var selectedPosition = $('#POSN_TITLE option:selected').val().substr(-3)
      console.log("here1");
      if((wls6 >= 0 || wls5 >= 0) && (selectedPosition == "(6)" || selectedPosition =="(5)")){
        console.log("imhere");
        $('#POSN_TITLE option').eq(wls6).prop('disabled', true);
        $('#POSN_TITLE option').eq(wls5).prop('disabled', true);
        $("#POSN_TITLE").val(1);
        $('.selectpicker').selectpicker('refresh');
      }
      if((selectedPosition != "(6)" || selectedPosition !="(5)") && (wls6 >= 0 || wls5 >= 0)){
        console.log("here3");
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
  var hour = document.getElementById("weeklyHours").value;
  if (hour == "20") {
      $('#OverloadModal').modal('show');
      $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
    }
};
function fillHoursPerWeek(fillhours=""){ // prefill hours per week select picker)
 var selectedHoursPerWeek = document.getElementById("weeklyHours");
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
  console.log("here 1")
  var oldValue = $("#modifyLSF").find(".oldValue"); //returns a nodeList where you need to access by index  aka console.log(thing[0]);
  var newValue = $("#modifyLSF").find("select.newValue, textarea.newValue, input.newValue");
  var effectiveDate = document.getElementById("datetimepicker0").value;
  var notesOld = document.getElementById("oldNotes").value;
  var notesNew = document.getElementById("supervisorNotes").value;
  for (var i=0; i < newValue.length; i=i+1) {
    console.log(i);
    console.log(oldValue[i].value);
    console.log(newValue[i].value);
    newVal = $(newValue[i]).val();
    console.log(newVal)
    if (oldValue[i].value != newVal && newVal != "") { //If the oldValue differs from the newValue, add it to the dictionary
      finalDict[newValue[i].id] = {"oldValue": oldValue[i].value,
                                     "newValue": newVal,
                                     "date": effectiveDate
                                  }
      }
  }
  if (notesOld != notesNew) { //Adds notes to dictionary if theyre different
    finalDict["supervisorNotes"] = {"oldValue": notesOld,
                                   "newValue": notesNew,
                                   "date": effectiveDate
                                  }
  }
  console.log(finalDict)
  console.log(JSON.stringify(finalDict));
  if (JSON.stringify(finalDict) !== '{}'){
    $('#submitModal').modal('show');
    console.log("hih")
    return finalDict
  }
  if (JSON.stringify(finalDict) == '{}'){
    console.log(JSON.stringify(finalDict));
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
