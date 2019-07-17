$(document).ready( function(){
x = $('#departmentsTable')
//console.log(x);
x.DataTable( {
'ordering': true
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
        category = "success"
        msg = "Department compliance changed";
        $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
        $("#flasher").delay(1000).fadeOut()
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
