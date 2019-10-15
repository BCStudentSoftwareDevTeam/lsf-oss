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
$(document).ready(function(){
   var department = document.getElementById("Department").value;
   var url = "/modifyLSF/getPosition/" + department;
       $.ajax({
         url: url,
         dataType: "json",
         success: function (response){
            fill_positions(response)
         }
       })
 });
$(document).ready(function(){
   var termcode = document.getElementById("termCode").value;
   var specificTerm = termcode.toString().substr(-2);
   if (specificTerm != 11 && specificTerm != 12 && specificTerm != 00){
     document.getElementById("jobType").disabled = true;
     $("#contractHoursDiv").show();
   }
   else{
     $("#weeklyHoursDiv").show();
   }
});
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
function positioncheck(){
  try{
    var position =$("#POSN_TITLE").val();
    var jobType = $("#jobType").val();
    if (jobType == "Primary"){
      $('#POSN_TITLE').find('option[value="TA (6)"]').prop("disabled", false);
      $('#POSN_TITLE').find('option[value="TA (5)"]').prop("disabled", false);
      $('.selectpicker').selectpicker('refresh');
    }
    var wls = position[position.length -2]
    if (jobType == "Secondary" && (wls == "6" || wls == "5" )){
      $('#POSN_TITLE').find('option[value="TA (6)"]').prop("disabled", true);
      $('#POSN_TITLE').find('option[value="TA (5)"]').prop("disabled", true);
      $("#POSN_TITLE").val(1);
      $('.selectpicker').selectpicker('refresh');
    }
    if (jobType == "Secondary" && (wls !== "6" || wls !== "5" )){
      $('#POSN_TITLE').find('option[value="TA (6)"]').prop("disabled", true);
      $('#POSN_TITLE').find('option[value="TA (5)"]').prop("disabled", true);
      $('.selectpicker').selectpicker('refresh');
    }
    if (jobType == "Primary" && (wls !== "6" || wls !== "5")){
      $('#POSN_TITLE').find('option[value="TA (6)"]').prop("disabled", false);
      $('#POSN_TITLE').find('option[value="TA (5)"]').prop("disabled", false);
      $('.selectpicker').selectpicker('refresh');
    }
  }
  catch(err){
    console.log(err)
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
    // $("#NochangeModal").css("z-index", parseInt($('.modal-backdrop').css('z-index')) + 1);
    console.log("here")
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
