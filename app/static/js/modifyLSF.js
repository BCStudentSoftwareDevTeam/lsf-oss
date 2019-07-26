$("#datetimepicker0").datepicker(); //Console says this is a type error but it still works?
$('.glyphicon-calendar').click(function() {
    $("#datetimepicker0").focus();
  });
var finalDict = {};
function buttonListener () {/////////YO THIS IS VERY FRAGILE!!!! Notes MUST be last or it will break. be mindful of this. -Kat and Bri
  var oldValue = $("#modifyLSF").find(".oldValue"); //returns a nodeList where you need to access by index  aka console.log(thing[0]);
  var newValue = $("#modifyLSF").find(".newValue");
  var effectiveDate = $("#datetimepicker0").datepicker("getDate");
  console.log(effectiveDate);
  for (var i=0; i < newValue.length-2; i=i+2) {
    // console.log(i/2);
    // console.log(oldValue[i/2].value);
    // console.log(newValue[i+1].value);
      newVal = $(newValue[i+1]).val();
    // } catch(err) {
    //   newVal = document.getElementById("Notes").value;
    // }
    console.log(newVal)
    if (oldValue[i/2].value != newVal) {
      finalDict[newValue[i+1].id] = {"oldValue": oldValue[i/2].value,
                                     "newValue": newVal,
                                     "date": effectiveDate.value
                                    }
      //   console.log(oldValue[i/2].value)
      //   console.log(newValue[i+1])
    }
    // TODO: HANDLE NOTES AND DATES
    console.log(finalDict)
  }
}

// function updateFormModifiedTable(fieldsModifiedDictionary){
//   //saves the following to modified form table:
//   //modifidFormID (primary key, auto increment), fieldModified, oldValue, newValue, effectiveDate (from form)
//   //parses through dictionary
//   for (var key in fieldsModifiedDictionary){
//     var value = dict[key];
//   }
//   //saving the old/new values to the appropriate field modified
// }

// function postModifications(laborStatusFormID){
//   //passes form attributes into a dictionary for ajax, posts to db, redirects\
//   console.log("postModifications called");
//   var formModifications = {} //For passing into Ajax data field (multiple attributes to pass)
//   //student cannot be changed
//   formModifications["primarySupervisor"] = document.getElementById('Supervisor').value; //FIX ME: NOT ALWAYS A PRIMARY SUPERVISOR. ITS DEPENDENT ON JOB TYPE
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
