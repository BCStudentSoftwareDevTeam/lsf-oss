
table=$("#studentList").DataTable({
  "drawCallback": function( settings ) {
    $("#studentList thead").remove(); } ,


     "order": [[0, "asc"]], //display order on column
     "pagingType": "simple_numbers",
     "ordering": false,
     "info": false,
     "lengthChange": false,

})
