$("#datetimepicker0").datepicker(); //Console says this is a type error but it still works?
$('.glyphicon-calendar').click(function() {
    $("#datetimepicker0").focus();
  });

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

function detectModifications(){
  //Checks fields for changes to determine what needs to be safed to modified form
  //modifidFormID (primary key), fieldModified, oldValue, newValue, effectiveDate (from form)
  var supervisorfield = document.getElementById("Supervisor");
  supervisorfield.addEventListener("input", function () {
    console.log("supervisorfield has changed!");
    });
  var positionfield = document.getElementById("Position");
  positionfield.addEventListener("input", function () {
    console.log("positionfield has changed!");
    });
  var wlsfield = document.getElementById("WLS");
  wlsfield.addEventListener("input", function () {
    console.log("wlsfield has changed!");
    });
  var jobtypefield = document.getElementById("JobType");
  jobtypefield.addEventListener("input", function () {
    console.log("jobtypefield has changed!");
    });
  var hoursfield = document.getElementById("Hours");
  hoursfield.addEventListener("input", function () {
    console.log("hoursfield has changed!");
    });
  var dateneededfield = document.getElementById("datetimepicker0");
  dateneededfield.addEventListener("input", function () {
    console.log("dateneededfield has changed!");
    });
  var notesfield = document.getElementById("Notes");
  notesfield.addEventListener("input", function () {
    console.log("notesfield has changed!");
    });
}
