$("#datetimepicker0").datepicker(); //Console says this is a type error but it still works?
$('.glyphicon-calendar').click(function() {
    $("#datetimepicker0").focus();
  });

function buildFieldList(){
  //builds fields for matching with appropriate values
  var fieldList = ["Supervisor","Position","WLS","JobType","Hours","Notes"]
  console.log("here's your fields");
  console.log(fieldList);
  return fieldList
}
function pullOldValues(){
  //Pull old values from hidden tags in html
  var oldValue = $("#modifyLSF").find(".oldValue"); //returns a nodeList where you need to access by index  aka console.log(thing[0]);
  // console.log("Here's the old values:");
  // console.log(oldValue[1]);
  var listOldValues = []
  for (var i=0; i < oldValue.length; i++) {
    var actualOldValues = oldValue[i].value;
    //console.log(actualOldValues);
    listOldValues.push(actualOldValues);
  }
  //console.log(listOldValues);
  return listOldValues
}

function pullNewValues(){
  //pulls new values from newValue class in HTML
  var newValue = $("#modifyLSF").find(".newValue");
  var listNewValues = []
  for (var i=1; i < newValue.length; i=i+2) {
     actualNewValues = $(newValue[i]).children("option:selected").val();
     //console.log(actualNewValues);
     listNewValues.push(actualNewValues);
   }
   //console.log(listNewValues);
   var newNoteValue = document.getElementById("Notes").value;
   listNewValues.push(newNoteValue);
   //console.log(listNewValues);
   return listNewValues
}

function constructFieldsModifiedDictionary(){
//takes old values and new values and comares them; if theyre new, add it to the dictionary
//dictionary key:field modified value: oldvalue, newvalue, effectiveDate
  var field = "the field"
  //fixme: pull those fields
  // var bothValues = [oldValue,newValue];
  // console.log("Here's both values:");
  // console.log(bothValues[0]);
  var fieldPairedWithValues = {} ; //for initial comparison; field: old value, new value
  // fieldWithValues["field"] : bothValues; //setting up field key with bothValues as the value
  //
  // //Should there be a for loop to parse through these elements?
  // //should there be an old/new for every element through indidivual variables?
  // //aka supervisoroldvalue, notesoldvalue....
  // //put those in a list and parse them????? doin a confusion -Kat
  // //
  //
  // var fieldsModifiedDictionary = {} ; //field, oldvalue, new value, effective date
  // for i in fieldWithValues{
  //     if (oldValue == newValue){ //if the value has not changed
  //       //pass aka do nothing aka this commented out line
  //     }
  //     else { //add to fieldsModifiedDictionary
  //
  //     }
  //   }
  // }
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

function postModifications(laborStatusFormID){
  //passes form attributes into a dictionary for ajax, posts to db, redirects\
  console.log("postModifications called");
  var formModifications = {} //For passing into Ajax data field (multiple attributes to pass)
  //student cannot be changed
  formModifications["primarySupervisor"] = document.getElementById('Supervisor').value; //FIX ME: NOT ALWAYS A PRIMARY SUPERVISOR. ITS DEPENDENT ON JOB TYPE
  //department cannot be changed
  formModifications["position"] = document.getElementById('Position').value;
  formModifications["WLS"] = document.getElementById('WLS').value;
  formModifications["jobtype"] = document.getElementById('JobType').value;
  //Term cannot be changed
  formModifications["weeklyHours"] = document.getElementById('Hours').value; //FIX ME: WILL NOT ALWAYS BEEN WEEKLY H(OURS COULD BE CONTRACT)
  formModifications["effectiveDate"] = document.getElementById('datetimepicker0').value;
  formModifications["laborSupervisorNotes"] = document.getElementById('Notes').value;
  //How to handle modifiedForm fields such as field modified, old value, and new value?
  //What happens when muliple fields are modified??
  var url = '/saveChanges/'+getFormId();
       $.ajax({
           type: "POST",
              url: url,
              data: formModifications,     //Dictionary pass
              dataType: 'json',
              success: function(response){
                      window.location = "/index" //FIXME: should we go to Supervisor portal or back to that student's labor history?
                       createTimestamp() ; //FIX ME: should add to form history bot just create a timestamp
              },
              error: function(error){
                  console.log("ERROR")
                  window.location.assign("/modifyLSF/formID")
              }
       });
}
