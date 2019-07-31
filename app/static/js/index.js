// function myfunction(apple){
//   console.log(apple)
// }

$(document).ready( function(){
  table=$("#studentList").DataTable({
    "drawCallback": function( settings ) {
      $("#studentList thead").remove(); } ,


     "order": [[0, "desc"]], //display order on column
     "pagingType": "simple_numbers",
     "ordering": false,
     "info": false,
     "lengthChange": false,
  })
});


// show the sub-sidebar only on this page
$("div.laborStudentChoice").show();


document.getElementById("current").addEventListener("click",function(){

    $(currentStu).show();
    $(pastStu).hide();

    $(".pastStu").attr("disabled", true)
    $(".actStu").removeAttr("disabled")
    $('#portalTitle').text("Current Students")


}, false);
document.getElementById("past").addEventListener("click",function(){
  $(currentStu).hide();
  $(pastStu).show();
  $(".actStu").attr("disabled", true)
  $(".pastStu").removeAttr("disabled")
  $('#portalTitle').text("Past Students")
}, false);
document.getElementById("all").addEventListener("click",function(){
  $(currentStu).show();
  $(pastStu).show();
  $(".pastStu").removeAttr("disabled")
  $(".actStu").removeAttr("disabled")
  $('#portalTitle').text("All Students")
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
