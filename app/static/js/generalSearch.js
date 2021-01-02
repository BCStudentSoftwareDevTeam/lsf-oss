$(document).ready(function(){
  $('#generalSearchTable').hide();
});

$('a.hover_indicator').click(function(e){
  e.preventDefault(); // prevents click on '#' link from jumping to top of the page.
});

$('#generalSearchButton').on('click', function(){

  $('#generalSearchTable').show();

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

  // TODO: If no option is selected tell user that they should have at least one input.
  // If at least one field is filled: run the ajax
  // otherwise, show a warning. 

  $('#generalSearchTable').DataTable({
        responsive: true,
        destroy: true,
        searching: false,
        processing: true,
        serverSide: true,
        paging: true,
        lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
        pageLength: 25,
        aaSorting: [[0, 'desc']],
        columnDefs: [{
          targets: -1,
          orderable: false,
        }],
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
