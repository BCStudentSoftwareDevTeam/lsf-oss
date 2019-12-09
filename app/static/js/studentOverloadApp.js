// checking the classification of student on page load
$(document).ready(function () {
  console.log($("#Classification").val())
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
function checkBoxCheck(obj){
  if(obj.checked == true){
      checkboxCounter = checkboxCounter + 1;
  }
  else if(obj.checked == false){
      checkboxCounter = checkboxCounter - 1;
  }
  if(checkboxCounter >= 8){
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
  console.log("here2")
  console.log($("#notes").val())
  if($("#notes").val() != "") {
    console.log("here1")
    $('#submitModal').modal('show');
  }
}

function updateDatabase(formID){
  console.log("Inside funciton");
  var notes = $("#notes").val()
  var dataDict = {}
  dataDict[formID] = {"Notes": notes}
  data = JSON.stringify(dataDict)
  console.log(data)
  var url = "/studentOverloadApp/update";
   $.ajax({
     url: url,
     method: "POST",
     data: data,
     dataType: "json",
     contentType: 'application/json',
     success: function (){
        console.log("successful response");
     }
   })
}
