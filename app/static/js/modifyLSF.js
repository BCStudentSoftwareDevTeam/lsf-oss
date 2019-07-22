function date() {

}

var j = jQuery.noConflict();
  j( function() {
      j( "#datetimepicker0" ).datepicker();
  } );


$('.glyphicon-calendar').click(function() {
    $("#datetimepicker0").focus();
  });

function postModifications(formID){
//passes form attributes into a dictionary for ajax, posts to db, redirects\
console.log("postModifications called");
var formModifications {} //For passing into Ajax data field (multiple attributes to pass)
//student cannot be changed
formModifications["primarySupervisor"] = document.getElementById('Supervisor').value; //FIX ME: NOT ALWAYS A PRIMARY SUPERVISOR. ITS DEPENDENT ON JOB TYPE
//department cannot be changed
formModifications["position"] = document.getElementById('Position').value;
formModifications["WLS"] = document.getElementById('WLS').value;
formModifications["jobtype"] = document.getElementById('JobType').value;
//Term cannot be changed
formModifications["weeklyHours"] = document.getElementById('Hours').value; //FIX ME: WILL NOT ALWAYS BEEN WEEKLY H(OURS COULD BE CONTRACT)
formModifications["effective date"] = document.getElementById('datetimepicker0').value;
formModifications["laborSupervisorNotes"] = document.getElementById('Notes').value;

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
