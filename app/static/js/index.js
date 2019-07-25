
table=$("#studentList").DataTable({
  "drawCallback": function( settings ) {
    $("#studentList thead").remove(); } ,


     "order": [[0, "desc"]], //display order on column
     "pagingType": "simple_numbers",
     "ordering": false,
     "info": false,
     "lengthChange": false,

})

// show the sub-sidebar only on this page
$("div.laborStudentChoice").show();
$(pastStu).hide();

document.getElementById("current").addEventListener("click",function(){
  $(currentStu).show();
  $(pastStu).hide();
}, false);
document.getElementById("past").addEventListener("click",function(){
  $(currentStu).hide();
  $(pastStu).show();
}, false);
document.getElementById("all").addEventListener("click",function(){
  $(currentStu).show();
  $(pastStu).show();
}, false);


$('.openBtn').on('click',function(){
    $('.modal-body').load('index.html',function(){
        $('#downloadModal').modal({show:true});
    });
});
