$(document).ready( function(){
x = $('#departmentsTable')
//console.log(x);
x.DataTable( {
'ordering': true
  });

});

function status(department) {
  //alert("Testing stuff");
  var departmentID = "#" + department
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
