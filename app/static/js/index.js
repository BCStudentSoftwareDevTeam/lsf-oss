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
}, false);
document.getElementById("past").addEventListener("click",function(){
  $(currentStu).hide();
  $(pastStu).show();
}, false);
document.getElementById("all").addEventListener("click",function(){
  $(currentStu).show();
  $(pastStu).show();
}, false);

// Listen for click on toggle checkbox
$('#select-all').click(function(event) {
    if(this.checked) {
        // Iterate each checkbox
        $(':checkbox').each(function() {
            this.checked = true;
        });
    } else {
        $(':checkbox').each(function() {
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
  console.log();
  window.location.href = '/static/LaborStudent.csv';//'/excel/';
  console.log("ok");
}

// $(document).ready(function(){
//        $('input[type="checkbox"]').click(function(){
//            if($(this).prop("checked") == true){
//                value = $('.S').val();
//                console.log(value);
//            }
//            else if($(this).prop("checked") == false){
//                console.log(value);
//            }
//        });
// });
//
//
// function laborStudent(obj){
//   var value = obj.value
//   console.log(value)
//   $.ajax({
//     type: "GET"
//     url: "/index/getStudent/" + value,
//     dataType: "jason",
//   })
// }
