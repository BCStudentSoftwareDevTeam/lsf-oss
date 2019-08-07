// function myfunction(apple){
//   console.log(apple)
// }
$(document).ready(function() {
  table
    .columns( 1 )
    .search("Current Students")
    .draw();
});

var table = $("#studentList").DataTable({
  "drawCallback": function( settings ) {
    $("#studentList thead").remove(); } ,


   "order": [[0, "desc"]], //display order on column
   "pagingType": "simple_numbers",
   "ordering": false,
   "info": false,
   "lengthChange": false,
   buttons: ['excel']

})



// show the sub-sidebar only on this page
$("div.laborStudentChoice").show();


document.getElementById("current").addEventListener("click",function(){
    $(".currentStu").show();
    $(".departmentStudents").hide();
    $(".pastStu").hide();

    table
      .columns( 1 )
      .search("Current Students")
      .draw();

    $(".pastStudentModal").attr("disabled", true)
    $(".currentStudentModal").removeAttr("disabled")
    $('#portalTitle').text("Current Students")
}, false);
document.getElementById("past").addEventListener("click",function(){
  $(".currentStu").hide();
  $(".departmentStudents").hide();
  $(".pastStu").show();

  table
    .columns( 1 )
    .search("Past Students")
    .draw();

  $(".currentStudentModal").attr("disabled", true)
  $(".pastStudentModal").removeAttr("disabled")
  $('#portalTitle').text("Past Students")
}, false);
document.getElementById("all").addEventListener("click",function(){
  $(".currentStu").show();
  $(".departmentStudents").hide();
  $(".pastStu").show();

  table
    .columns( 1 )
    .search("Current Students|Past Students", true, false, true)
    .draw();

  $(".pastStudentModal").removeAttr("disabled")
  $(".currentStudentModal").removeAttr("disabled")
  $('#portalTitle').text("All Students")
}, false);
document.getElementById("department").addEventListener("click",function(){
  $(".departmentStudents").show();
  $(".currentStu").hide();
  $(".pastStu").hide();

  table
    .columns( 1 )
    .search("Department Students")
    .draw();

  $(".currentStudentModal").attr("disabled", true)
  $(".pastStudentModal").attr("disabled", true)
  $('#portalTitle').text("Department Students")
}, false);

// Listen for click on toggle checkbox
$('#select-all').click(function(event) {
    if(this.checked) {
        // Iterate each checkbox
        $(':checkbox').not("[disabled]").each(function() {
            this.checked = true;
        });
    } else {
        $(':checkbox').not("[disabled]").each(function() {
            this.checked = false;
        });
    }
});

$('.openBtn').on('click',function(){
    $('.modal-body').load('index.html',function(){
        $('#downloadModal').modal({show:true});
    });

});

function downloadHistory(){
  $('input[type="checkbox"]:checked').prop('checked',false);

}
