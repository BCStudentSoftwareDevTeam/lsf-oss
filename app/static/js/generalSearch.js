// var termCode = $("#termSelect").val();
// var departmentID = $("#departmentSelect").val();
// var supervisorID = $("#supervisorSelect").val();
// var studentID = $("#studentSelect").val();
// var formStatusList = [];
// var formTypeList = [];
//
// $("input:checkbox[name='formStatus']:checked").each(function(){
//     formStatusList.push($(this).val());
// });
//
// $("input:checkbox[name='formType']:checked").each(function(){
//     formTypeList.push($(this).val());
// });

$('#generalSearchButton').on('click', function(){
  var myTable = $('#generalSearchTable').DataTable({
        // "pageLength": 10,
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/admin/generalSearch",
            "type": "POST",
            "dataType": "json",
            "dataSrc": "data",
        },
        "columns": [
            {"data": "Term"},
            {"data": "Department"},
            {"data": "Supervisor"},
            {"data": "Students"},
            {"data": "Position"},
            {"data": "Hours"},
            {"data": "Contract Dates"},
            {"data": "Created"},
            {"data": ""},
        ],
        "dataSrc": function (d) {
            // Format API response for DataTables
            var response = d;
            if (typeof d.response != 'undefined') {
                response = d.response;
            }
            console.log("response!!!");
            console.log(JSON.stringify(response)); // Output from this is below...
            return response.data;
        },
  });
});



  // queryDict = {'termCode': termCode,
  //              'departmentID': departmentID,
  //              'supervisorID': supervisorID,
  //              'studentID': studentID,
  //              'formStatus': formStatusList,
  //              'formType': formTypeList
  //            };

  // var data = JSON.stringify(queryDict);
//   $.ajax({
//     method: "POST",
//     url: url,
//     data: data,
//     contentType: "application/json",
//     success: function(response) {
//       console.log("Success");
//     }
//   });
// //
// });
