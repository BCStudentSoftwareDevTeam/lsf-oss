$("#datetimepicker0").datepicker();
$('.glyphicon-calendar').click(function() {
    $("#datetimepicker0").focus();
});
// function hideFiveHourOption(){
// // This is for hiding the 0-5 option of primary is selected for job Type
//   var jobType = document.getElementById("JobType");
//   var hours = document.getElementById("Hours");
//   if (jobType.value == "Primary"){
//     hours.options[0].disabled;
//     console.log("0-5 should be disabled...");
//   }
// }



var effectiveDate = $("#datetimepicker0").datepicker('getDate');
var finalDict = {}; //This is for buttonListener /modified fields to be saved to modform table
function buttonListener () {
  //YOOOO THIS IS VERY FRAGILE!!!! Notes MUST be last or it will break. be mindful of this. -Kat and Bri
  var oldValue = $("#modifyLSF").find(".oldValue"); //returns a nodeList where you need to access by index  aka console.log(thing[0]);
  var newValue = $("#modifyLSF").find(".newValue");
  var effectiveDate = document.getElementById("datetimepicker0").value; //this doesnt work since value is prefilldateneeded and..thats nothing
  console.log(effectiveDate);
  for (var i=0; i < newValue.length-2; i=i+2) { //since newValue class is put on the div AND the select.. we skipped the div objects
    // console.log(i/2);
    // console.log(oldValue[i/2].value);
    // console.log(newValue[i+1].value);
      newVal = $(newValue[i+1]).val();
    // } catch(err) {
    //   newVal = document.getElementById("Notes").value; //TODO: fix this lmao
    // }
    console.log(newVal)
    if (oldValue[i/2].value != newVal) {     //If the oldValue differs from the newValue, add it to the dictionary
      finalDict[newValue[i+1].id] = {"oldValue": oldValue[i/2].value,
                                     "newValue": newVal,
                                     "date": effectiveDate
                                    }
      //   console.log(oldValue[i/2].value)
      //   console.log(newValue[i+1])
    }
    console.log(finalDict)
  }
}

// function updateFormModifiedTable(finalDict){
//   //saves the following to modified form table:
//   //modifidFormID (primary key, auto increment), fieldModified, oldValue, newValue, effectiveDate (from form)
//   //parses through dictionary
//   for (var key in finalDict){
//     var value = dict[key];
//   }
//   //saving the old/new values to the appropriate field modified
// }

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
//   //How to handle modifiedForm fields such as field modified, old value, and new value?
//   //What happens when muliple fields are modified??
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
