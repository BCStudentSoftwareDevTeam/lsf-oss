$("#contractHours").hide();
$("#hoursPerWeek").hide();
$("#datetimepicker0").datepicker();
// $("#datetimepicker0").datepicker("setDate", new Date()); //Sets datepicker to todays date by default
$("#datetimepicker0").datepicker({startDate: new Date()});
// $("#datetimepicker0").datepicker({ minDate: 0 })
//FIXME: add a contstraint that does not allow user to set date before today's date
$('.glyphicon-calendar').click(function() {
    $("#datetimepicker0").focus();
});
function fill_positions(response) {
  var selected_positions = document.getElementById("Position");
    for (var key in response) {
      var options = document.createElement("option");
      options.text = response[key]["position"].toString() + " " + "(" + response[key]["WLS"].toString() + ")"
      options.value = key;
      selected_positions.appendChild(options);
    $('.selectpicker').selectpicker('refresh');
  }
}
$(document).ready(function(){
   var department = document.getElementById("Department").value;
   var url = "/modifyLSF/getPositions/" + department;
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
     document.getElementById("JobType").disabled = true;
     $("#contractHours").show();
   }
   else{
     $("#hoursPerWeek").show();
   }
});
// Pops up a modal for overload
function hourscheck(){
  var hour = document.getElementById("Hours").value;
  console.log(hour)
  if (hour == "20") {
      $('#OverloadModal').modal('show');
      $('#overloadModalButton').attr('data-target', '') // prevent a Primary Modal from showing up
    }
};
//////////Modified form check and dictionary creation////////////
//Structure: {[field]:{[oldValue],[newValue],[effective date]}}
var effectiveDate = $("#datetimepicker0").datepicker('getDate');
var finalDict = {};
function buttonListener () {
  //YOOOO THIS IS VERY FRAGILE!!!! Notes MUST be last or it will break. be mindful of this. -Kat and Bri
  var oldValue = $("#modifyLSF").find(".oldValue"); //returns a nodeList where you need to access by index  aka console.log(thing[0]);
  var newValue = $("#modifyLSF").find(".newValue");
  var effectiveDate = document.getElementById("datetimepicker0").value;
  //Do we need to pull the notes FIELD (ID) separate as well? (its the key for the outer dict..)
  var notesOld = document.getElementById("oldNotes").value; //TODO: add this to oldValue
  var notesNew = document.getElementById("Notes").value;//TODO: add this to newValue
  console.log("notesOld"+notesOld);
  console.log("notesNew"+notesNew);
  for (var i=0; i < newValue.length-2; i=i+2) { //since newValue class is put on the div AND the select.. we skipped the div objects
    // console.log(i/2);
    // console.log(oldValue[i/2].value);
    // console.log(newValue[i+1].value);
      newVal = $(newValue[i+1]).val();
    console.log(newVal)
    if (oldValue[i/2].value != newVal) { //If the oldValue differs from the newValue, add it to the dictionary
      finalDict[newValue[i+1].id] = {"oldValue": oldValue[i/2].value,
                                     "newValue": newVal,
                                     "date": effectiveDate
                                    }
      }
  }
  if (notesOld != notesNew) { //Adds notes to dictionary if theyre different
    finalDict["Notes"] = {"oldValue": notesOld,
                                   "newValue": notesNew,
                                   "date": effectiveDate
                                  }

  }
  console.log(finalDict)
}
//////////Saving to modifiedForm table/////////
// function updateFormModifiedTable(finalDict){
//   //saves the following to modified form table:
//   //modifidFormID (primary key, auto increment), fieldModified, oldValue, newValue, effectiveDate (from form)
//   //parses through dictionary
//   for (var key in finalDict){
//     var value = dict[key];
//   }
//   //saving the old/new values to the appropriate field modified
// }


///////////Saving to LSF table////////////
// function postModifications(laborStatusFormID){
//   //passes form attributes into a dictionary for ajax, posts to db, redirects\
//   console.log("postModifications called");
//   var formModifications = {} //For passing into Ajax data field (multiple attributes to pass)
//   //student cannot be changed
//   formModifications["supervisor"] = document.getElementById('Supervisor').value;
//   //department cannot be changed
//   formModifications["position"] = document.getElementById('Position').value;
//   formModifications["WLS"] = document.getElementById('WLS').value;
//   formModifications["jobtype"] = document.getElementById('JobType').value;
//   //Term cannot be changed
//   formModifications["weeklyHours"] = document.getElementById('Hours').value; //FIX ME: WILL NOT ALWAYS BEEN WEEKLY H(OURS COULD BE CONTRACT)
//   formModifications["effectiveDate"] = document.getElementById('datetimepicker0').value;
//   formModifications["laborSupervisorNotes"] = document.getElementById('Notes').value;
//   var url = '/saveChanges/'+getFormId();
//        $.ajax({
//            type: "POST",
//               url: url,
//               data: formModifications,     //Dictionary pass
//               dataType: 'json',
//               success: function(response){
//                       window.location = "/index" //FIXME: should we go to Supervisor portal or back to that student's labor history?
//                        createTimestamp() ; //FIX ME: should add to form history bot just create a timestamp
//               },
//               error: function(error){
//                   console.log("ERROR")
//                   window.location.assign("/modifyLSF/formID")
//               }
//        });
// }
