$(document).ready(function() {
  // When the page first loads, this function will make sure the data table is
  // only showing the correct buttons and data
  table
    .columns( 1 )
    .search("My Current Students")
    .draw();

  $("#currentDepartmentStudents").hide()
  $("#allDepartmentStudents").hide()
  $("#userDepartments").hide()
  $("#placeholder").show()

  $(".currentStu").show();
  $(".allDeptStu").hide();
  $(".currentDeptStu").hide();
  $(".pastStu").hide();
  $(".pastStudentModal").attr("disabled", true);
  $(".allDepartmentModal").attr("disabled", true);
  $(".currentDepartmentModal").attr("disabled", true);
  $(".currentStudentModal").removeAttr("disabled");
  $('#portalTitle').text("Current Students");
  $("#myCurrentStudents").removeClass("btn-primary");
  $("#myCurrentStudents").addClass("btn-light");

});

var table = $("#studentList").DataTable({
  "drawCallback": function( settings ) {
    $("#studentList thead").remove(); } , // Used to hide the data table header
   "order": [[0, "desc"]], //display order on column
   "pagingType": "simple_numbers",
   "ordering": false,
   "info": false,
   "lengthChange": false,
   dom: 'Bfrtip',
   // Used to created the buttons rendered by the data table
   buttons: [
      {
        text: 'Current Only',
        action: function ( e, dt, node, config ) {
          // Used to enable and disable the correct checkboxes inside the modal
          // depending on the button pressed
          changeButtonColor("#myCurrentStudents")
          $(".currentStu").show();
          $(".allDeptStu").hide();
          $(".currentDeptStu").hide();
          $(".pastStu").hide();
          $(".pastStudentModal").attr("disabled", true);
          $(".allDepartmentModal").attr("disabled", true);
          $(".currentDepartmentModal").attr("disabled", true);
          $(".currentStudentModal").removeAttr("disabled");
          $('#portalTitle').text("Current Students");
          $("#myCurrentStudents").removeClass("btn-primary");
          $("#myCurrentStudents").addClass("btn-light");
          // Used to filter the datatable by the hidden column made in the HTML
          table
            .columns( 1 )
            .search("My Current Students")
            .draw();
         },
        attr: { id: "myCurrentStudents"}
      },
      {
        text: 'Past Only',
        action: function ( e, dt, node, config ) {
          // Used to enable and disable the correct checkboxes inside the modal
          // depending on the button pressed
          changeButtonColor("#myPastStudents")
          $(".currentStu").hide();
          $(".allDeptStu").hide();
          $(".currentDeptStu").hide();
          $(".pastStu").show();
          $(".currentStudentModal").attr("disabled", true);
          $(".allDepartmentModal").attr("disabled", true);
          $(".currentDepartmentModal").attr("disabled", true);
          $(".pastStudentModal").removeAttr("disabled");
          $('#portalTitle').text("Past Students");
          $("#myPastStudents").removeClass("btn-primary");
          $("#myPastStudents").addClass("btn-light");
          // Used to filter the datatable by the hidden column made in the HTML
          table
            .columns( 1 )
            .search("My Past Students")
            .draw();
         },
        attr: { id: "myPastStudents"}
      },
      {
        text: 'All',
        action: function ( e, dt, node, config ) {
          // Used to enable and disable the correct checkboxes inside the modal
          // depending on the button pressed
          changeButtonColor("#allMyStudents")
          $(".currentStu").show();
          $(".allDeptStu").hide();
          $(".currentDeptStu").hide();
          $(".pastStu").show();
          $(".pastStudentModal").removeAttr("disabled");
          $(".allDepartmentModal").attr("disabled", true);
          $(".currentDepartmentModal").attr("disabled", true);
          $(".currentStudentModal").removeAttr("disabled");
          $('#portalTitle').text("All Students");
          $("#allMyStudents").removeClass("btn-primary");
          $("#allMyStudents").addClass("btn-light");
          // Used to filter the datatable by the hidden column made in the HTML
          table
            .columns( 1 )
            .search("My Current Students|My Past Students", true, false, true)
            .draw();
         },
        attr: { id: "allMyStudents"}
      },
      {
        text: 'Current Only',
        action: function ( e, dt, node, config ) {
          // Used to enable and disable the correct checkboxes inside the modal
          // depending on the button pressed
          changeButtonColor("#currentDepartmentStudents")
          $(".currentStu").hide();
          $(".allDeptStu").hide();
          $(".currentDeptStu").show();
          $(".pastStu").hide();
          $(".currentStudentModal").attr("disabled", true);
          $(".allDepartmentModal").attr("disabled", true);
          $(".currentDepartmentModal").removeAttr("disabled");
          $(".pastStudentModal").attr("disabled", true);
          $('#portalTitle').text("Current Department Students");
          $("#currentDepartmentStudents").removeClass("btn-primary");
          $("#currentDepartmentStudents").addClass("btn-light");
          // Used to filter the datatable by the hidden column made in the HTML
          table
            .columns( 1 )
            .search("Current Department Students")
            .draw();
         },
        attr: { id: "currentDepartmentStudents"}
      },
      {
        text: 'All',
        action: function ( e, dt, node, config ) {
          // Used to enable and disable the correct checkboxes inside the modal
          // depending on the button pressed
          changeButtonColor("#allDepartmentStudents")
          $(".currentStu").hide();
          $(".allDeptStu").show();
          $(".currentDeptStu").hide();
          $(".pastStu").hide();
          $(".currentStudentModal").attr("disabled", true);
          $(".allDepartmentModal").removeAttr("disabled");
          $(".currentDepartmentModal").attr("disabled", true);
          $(".pastStudentModal").attr("disabled", true);
          $('#portalTitle').text("All Department Students");
          $("#allDepartmentStudents").removeClass("btn-primary");
          $("#allDepartmentStudents").addClass("btn-light");
          // Used to filter the datatable by the hidden column made in the HTML
          table
            .columns( 1 )
            .search("All Department Students")
            .draw();
         },
        attr: { id: "allDepartmentStudents"}
      }
    ],
  initComplete: function () {
    // Function used to remove the default class given to datatable buttons, and
    // give buttons bootstrap classes instead
    var btns = $('.dt-button');
    btns.addClass('btn btn-primary');
    btns.removeClass('dt-button');

    }

})

function changeButtonColor(ID) {
  var buttonID = ID
  if ($("#myPastStudents").hasClass("btn btn-light")){
    $("#myPastStudents").removeClass("btn btn-light");
    $("#myPastStudents").addClass("btn btn-primary");
  }
  if ($("#myCurrentStudents").hasClass("btn btn-light")){
    $("#myCurrentStudents").removeClass("btn btn-light");
    $("#myCurrentStudents").addClass("btn btn-primary");
  }
  if ($("#allMyStudents").hasClass("btn btn-light")){
    $("#allMyStudents").removeClass("btn btn-light");
    $("#allMyStudents").addClass("btn btn-primary");
  }
  if ($("#currentDepartmentStudents").hasClass("btn btn-light")){
    $("#currentDepartmentStudents").removeClass("btn btn-light");
    $("#currentDepartmentStudents").addClass("btn btn-primary");
  }
  if ($("#allDepartmentStudents").hasClass("btn btn-light")){
    $("#allDepartmentStudents").removeClass("btn btn-light");
    $("#allDepartmentStudents").addClass("btn btn-primary");
  }
  if ($(buttonID).hasClass("btn btn-light")){
    $(buttonID).addClass('btn btn-primary');
    $(buttonID).removeClass('btn btn-light');
  }
}

// show the sub-sidebar only on this page
$("div.laborStudentChoice").show();

document.getElementById("myStudents").addEventListener("click",function(){
  // When the 'My Students' tab in the sidebar is clicked, this Function
  // hides and shows the correct buttons for that page, filter the datatable,
  // and shows the correct checkboxes that should show in the modal
  $("#userDepartments").hide()
  $("#placeholder").show()
  $("#currentDepartmentStudents").hide()
  $("#allDepartmentStudents").hide()
  $("#myCurrentStudents").show()
  $("#myPastStudents").show()
  $("#allMyStudents").show()
  $('#portalTitle').text("Current Students");
  $("#myCurrentStudents").removeClass("btn-primary");
  $("#myCurrentStudents").addClass("btn-light");

  table
    .columns( 1 )
    .search("My Current Students")
    .draw();

  $(".currentStu").show();
  $(".allDeptStu").hide();
  $(".currentDeptStu").hide();
  $(".pastStu").hide();
  $(".pastStudentModal").attr("disabled", true);
  $(".allDepartmentModal").attr("disabled", true);
  $(".currentDepartmentModal").attr("disabled", true);
  $(".currentStudentModal").removeAttr("disabled");
  $('#portalTitle').text("Current Students");
}, false);

document.getElementById("department").addEventListener("click",function(){
  // When the 'My Department' tab in the sidebar is clicked, this Function
  // hides and shows the correct buttons for that page, filter the datatable,
  // and shows the correct checkboxes that should show in the modal
  $("#userDepartments").show()
  $("#placeholder").hide()
  $(".currentStu").hide();
  $(".allDeptStu").hide();
  $(".currentDeptStu").show();
  $(".pastStu").hide();
  $(".currentStudentModal").attr("disabled", true);
  $(".allDepartmentModal").attr("disabled", true);
  $(".currentDepartmentModal").removeAttr("disabled");
  $(".pastStudentModal").attr("disabled", true);
  $('#portalTitle').text("Current Department Students");
  $("#currentDepartmentStudents").removeClass("btn-primary");
  $("#currentDepartmentStudents").addClass("btn-light");

  table
    .columns( 1 )
    .search("Current Department Students")
    .draw();

  $("#currentDepartmentStudents").show()
  $("#allDepartmentStudents").show()
  $("#myCurrentStudents").hide()
  $("#myPastStudents").hide()
  $("#allMyStudents").hide()
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

// Shows the modal
$('.openBtn').on('click',function(){
    $('.modal-body').load('index.html',function(){
        $('#downloadModal').modal({show:true});
    });

});

function downloadHistory(){
  $('input[type="checkbox"]:checked').prop('checked',false);
}

function populateTable(){
  var departmentDropDown = document.getElementById("departmentDropDown");
  var departmentSelected = departmentDropDown.options[departmentDropDown.selectedIndex].value;
  $.ajax({
    method: "GET",
    url: "/main/department/" + departmentSelected,
    success: function(response) {
      console.log(response);
      $(".modal-body").append(response);
      $("#studentList tbody").append(response);
      // table.ajax.reload();
    }
  })
}
