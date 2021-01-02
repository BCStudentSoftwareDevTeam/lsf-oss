$('#generalSearchButton').on('click', function(){
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

  $('#generalSearchTable').DataTable({
        destroy: true,
        searching: false,
        processing: true,
        serverSide: true,
        paging: true,
        lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
        pageLength: 25,
        aaSorting: [[0, 'desc']],
        ajax: {
            url: "/admin/generalSearch",
            type: "POST",
            data: {'data': data},
            dataSrc: "data",
            columns: [
              {"data":"Term"},
              {"data":"Department"},
              {"data":"Supervisor"},
              {"data":"Student"},
              {"data":"Position (WLS)"},
              {"data":"Hours"},
              {"data":"Contract Dates"},
              {"data":"Created"},
              {"data":""}
            ]
        }
  });
});
