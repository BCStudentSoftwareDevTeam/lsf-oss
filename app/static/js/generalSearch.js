$(document).ready(function(){
  console.log("HELOOOOOOOO");
});

$("#generalSearchButton").on('click', function() {
  var termCode = $("#termSelect").val();
  var departmentID = $("#departmentSelect").val();
  var supervisorID = $("#supervisorSelect").val();
  var studentID = $("#studentSelect").val();
  var formStatusList = [];
  var formTypeList = [];

	$("input:checkbox[name='formStatus']:checked").each(function(){
      formStatusList.push($(this).val());
	});

  $("input:checkbox[name='formType']:checked").each(function(){
      formTypeList.push($(this).val());
	});

  queryDict = {'termCode': termCode,
               'departmentID': departmentID,
               'supervisorID': supervisorID,
               'studentID': studentID,
               'formStatus': formStatusList,
               'formType': formTypeList
             };

  var data = JSON.stringify(queryDict);
  var url  = "/admin/generalSearch/quwey"
  $.ajax({
    method: "POST",
    url: url,
    data: data,
    contentType: "application/json",
    success: function(response) {
      console.log("Success");
    }
  });
});
