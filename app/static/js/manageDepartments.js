// $.fn.dataTable.ext.type.order['compliance-status'] = function ( d ) {
//     switch ( d ) {
//         case 'In Compliance':    return 1;
//         case 'Not in Compliance': return 2;
//     }
//     return 0;
// };


$(document).ready( function(){
x = $('#departmentsTable')
//console.log(x);
x.DataTable( {
  // "columnDefs": [ {
  //     "type": "compliance-status",
  //     "targets": 1
  // } ]
});
});

function status(department) {

  $.ajax({
    method: "POST",
    url: "/admin/complianceStatus",
    dataType: "json",
    contentType: "application/json",
    data: JSON.stringify({"deptName": department}),
    processData: false,
    success: function(response) {
      console.log(response);
      if(response["Success"]) {
        category = "info"
        msg = "Department compliance changed.";
        $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
        $("#flasher").delay(3000).fadeOut()
        var departmentID = "#" + department;
        //console.log(departmentID);
        if ($(departmentID).hasClass("btn-success")){
          $(departmentID).removeClass("btn-success");
          $(departmentID).addClass("btn-danger");
          $(departmentID).text("Not in Compliance")
        }
        else {
          $(departmentID).removeClass("btn-danger");
          $(departmentID).addClass("btn-success");
          $(departmentID).text("In Compliance")
        }
    }
  }
    })
  };
