// checking the classification of student on page load
$(document).ready(function () {
  $("#notes").prop("disabled", true);
  $("#submit").hide();
  if ($("#Classification").val() == "Freshman"){
    $('#freshmanWarning').modal({
     backdrop: 'static',
     keyboard: false
  })
 }

});

checkboxCounter = 0; //keeps track of how many checkboxes are checked
function checkBoxCheck(obj,totalFormHours){
  console.log(totalFormHours)
  if(obj.checked == true){
      checkboxCounter = checkboxCounter + 1;
  }
  else if(obj.checked == false){
      checkboxCounter = checkboxCounter - 1;
  }
  if(checkboxCounter >= 8 & totalFormHours>=20){
    $("#notes").prop("disabled", false);
  }
  else if (checkboxCounter >=5 & totalFormHours <20){
      $("#notes").prop("disabled", false);
  }
  else{
    $("#notes").prop("disabled", true);
  }
}

function primaryCheck(){
  if(($("#notes").val() != "")){
    $("#submit").show();
  }
  else{
    $("#submit").hide();
  }
}

function checkForEmptyFields(){
  if($("#notes").val() != "") {
    $('#submitModal').modal('show');
  }
}

function updateDatabase(formID){
  var notes = $("#notes").val()
  var dataDict = {}
  dataDict[formID] = {"Notes": notes, "formID": formID}
  data = JSON.stringify(dataDict)
  var url = "/studentOverloadApp/update";
   $.ajax({
     url: url,
     method: "POST",
     data: data,
     dataType: "json",
     contentType: 'application/json'
   })
}
