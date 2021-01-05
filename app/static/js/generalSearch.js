$(document).ready(function(){
  $('#generalSearchTable').hide();
  $("#download").prop('disabled', true);
});

$('a.hover_indicator').click(function(e){
  e.preventDefault(); // prevents click on '#' link from jumping to top of the page.
});

$('#generalSearchButton').on('click', function(){

  var termCode = $("#termSelect").val();
  var departmentID = $("#departmentSelect").val();
  var supervisorID = $("#supervisorSelect").val();
  var studentID = $("#studentSelect").val();
  var formStatusList = [];
  var formTypeList = [];

  $("input:radio[name='formStatus']:checked").each(function(){
      formStatusList.push($(this).val());
  });

  $("input:radio[name='formType']:checked").each(function(){
      formTypeList.push($(this).val());
  });

  queryDict = {'termCode': termCode,
               'departmentID': departmentID,
               'supervisorID': supervisorID,
               'studentID': studentID,
               'formStatus': formStatusList,
               'formType': formTypeList
             };

  data = JSON.stringify(queryDict)

  if (termCode + departmentID + supervisorID + studentID == "" && formStatusList.length + formTypeList.length == 0) {
    $("#flash_container").html('<div class="alert alert-danger" role="alert" id="flasher">At least one field one must be selected.</div>');
    $("#flasher").delay(5000).fadeOut();
  }
  else {
    $("#download").prop('disabled', false);
    $('#generalSearchTable').show();
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
  }
});
