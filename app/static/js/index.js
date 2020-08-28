var table;
$(document).ready(function() {
  console.log(document.cookie);
  console.log(document.location.href);
  var url = document.location.href
  createButtons();
  if (url.endsWith('/')){
    console.log('My students');
    changeButtonColor("#myCurrentStudents")
    $("#userDepartments").hide()
    $("#placeholder").show()
    $("#currentDepartmentStudents").hide()
    $("#allDepartmentStudents").hide()
    $("#myCurrentStudents").show()
    $("#myPastStudents").show()
    $("#allMyStudents").show()
    $('#portalTitle').text("Current Students");
    $("#myCurrentStudents").removeClass("btn-light");
    $("#myCurrentStudents").addClass("btn-primary");


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
  } else {
    console.log('Inside of departments');
    changeButtonColor("#currentDepartmentStudents")
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
    $("#currentDepartmentStudents").removeClass("btn-light");
    $("#currentDepartmentStudents").addClass("btn-primary");

    table
      .columns( 1 )
      .search("Current Department Students")
      .draw();

    $("#currentDepartmentStudents").show()
    $("#allDepartmentStudents").show()
    $("#myCurrentStudents").hide()
    $("#myPastStudents").hide()
    $("#allMyStudents").hide()

    // If the select picker already has a department selected when the page is loaded,
    // then we want to populate the data table with the selected department
    var departmentDropDown = $("#departmentDropDown");
    console.log(departmentDropDown);
    var departmentSelected = $(departmentDropDown, 'option:selected').attr('value');
    console.log(departmentSelected);
    if (departmentSelected) {
      console.log(departmentSelected);
      populateTable();
    }
  }
  $('#studentList').show();
  $('#download').show();
  // When the page first loads, this function will make sure the data table is
  // only showing the correct buttons and data
  // table
  //   .columns( 1 )
  //   .search("My Current Students")
  //   .draw();
  //
  // $("#currentDepartmentStudents").hide()
  // $("#allDepartmentStudents").hide()
  // $("#userDepartments").hide()
  // $("#placeholder").show()
  //
  // $(".currentStu").show();
  // $(".allDeptStu").hide();
  // $(".currentDeptStu").hide();
  // $(".pastStu").hide();
  // $(".pastStudentModal").attr("disabled", true);
  // $(".allDepartmentModal").attr("disabled", true);
  // $(".currentDepartmentModal").attr("disabled", true);
  // $(".currentStudentModal").removeAttr("disabled");
  // $('#portalTitle').text("Current Students");
  // $("#myCurrentStudents").removeClass("btn-light");
  // $("#myCurrentStudents").addClass("btn-primary");

});
function createButtons(){

  table = $("#studentList").DataTable({
    "drawCallback": function( settings ) {
      $("#studentList thead").remove(); } , // Used to hide the data table header
    "columnDefs":[
      {"visable": false, "target": [1]}
    ],
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
            // Used to filter the datatable by the hidden column made in the HTML
            table
              .columns( 1 )
              .search("Current Department Students")
              .draw();
           },
          attr: { id: "currentDepartmentStudents"}
        },
        {
          text: 'Current and Past',
          action: function ( e, dt, node, config ) {
            // Used to enable and disable the correct checkboxes inside the modal
            // depending on the button pressed
            changeButtonColor("#allDepartmentStudents")
            $(".currentStu").hide();
            $(".allDeptStu").show();
            $(".currentDeptStu").show();
            $(".pastStu").hide();
            $(".currentStudentModal").attr("disabled", true);
            $(".allDepartmentModal").removeAttr("disabled");
            $(".currentDepartmentModal").removeAttr("disabled");
            $(".pastStudentModal").attr("disabled", true);
            $('#portalTitle').text("Current and Past Department Students");
            // Used to filter the datatable by the hidden column made in the HTML
            table
              .columns( 1 )
              .search("All Department Students|Current Department Students", true, false, true)
              .draw();
           },
          attr: { id: "allDepartmentStudents"}
        }
      ],
    initComplete: function () {
      // Function used to remove the default class given to datatable buttons, and
      // give buttons bootstrap classes instead
      var btns = $('.dt-button');
      btns.addClass('btn btn-light');
      btns.removeClass('dt-button');

      }

  })
}


function changeButtonColor(ID) {
  var buttonID = ID
  var buttonIDList = ["#myPastStudents", "#myCurrentStudents", "#allMyStudents",
    "#currentDepartmentStudents", "#allDepartmentStudents"]
  for (i = 0; i < buttonIDList.length; i++){
    $(buttonIDList[i]).removeClass("btn btn-primary");
    $(buttonIDList[i]).addClass("btn btn-light");
  }

  $(buttonID).removeClass('btn btn-light');
  $(buttonID).addClass('btn btn-primary');
}

// show the sub-sidebar only on this page
$("div.laborStudentChoice").show();

// $("#myStudents").on("click keypress",function(){
//   // When the 'My Students' tab in the sidebar is clicked, this Function
//   // hides and shows the correct buttons for that page, filter the datatable,
//   // and shows the correct checkboxes that should show in the modal
//   console.log("here");
//   changeButtonColor("#myCurrentStudents")
//   $("#userDepartments").hide()
//   $("#placeholder").show()
//   $("#currentDepartmentStudents").hide()
//   $("#allDepartmentStudents").hide()
//   $("#myCurrentStudents").show()
//   $("#myPastStudents").show()
//   $("#allMyStudents").show()
//   $('#portalTitle').text("Current Students");
//   $("#myCurrentStudents").removeClass("btn-light");
//   $("#myCurrentStudents").addClass("btn-primary");
//
//
//   table
//     .columns( 1 )
//     .search("My Current Students")
//     .draw();
//
//   $(".currentStu").show();
//   $(".allDeptStu").hide();
//   $(".currentDeptStu").hide();
//   $(".pastStu").hide();
//   $(".pastStudentModal").attr("disabled", true);
//   $(".allDepartmentModal").attr("disabled", true);
//   $(".currentDepartmentModal").attr("disabled", true);
//   $(".currentStudentModal").removeAttr("disabled");
//   $('#portalTitle').text("Current Students");
// });

// $("#department").on("click keypress", function(e){
//   // When the 'My Department' tab in the sidebar is clicked, this Function
//   // hides and shows the correct buttons for that page, filter the datatable,
//   // and shows the correct checkboxes that should show in the modal
//   changeButtonColor("#currentDepartmentStudents")
//   $("#userDepartments").show()
//   $("#placeholder").hide()
//   $(".currentStu").hide();
//   $(".allDeptStu").hide();
//   $(".currentDeptStu").show();
//   $(".pastStu").hide();
//   $(".currentStudentModal").attr("disabled", true);
//   $(".allDepartmentModal").attr("disabled", true);
//   $(".currentDepartmentModal").removeAttr("disabled");
//   $(".pastStudentModal").attr("disabled", true);
//   $('#portalTitle').text("Current Department Students");
//   $("#currentDepartmentStudents").removeClass("btn-light");
//   $("#currentDepartmentStudents").addClass("btn-primary");
//
//   table
//     .columns( 1 )
//     .search("Current Department Students")
//     .draw();
//
//   $("#currentDepartmentStudents").show()
//   $("#allDepartmentStudents").show()
//   $("#myCurrentStudents").hide()
//   $("#myPastStudents").hide()
//   $("#allMyStudents").hide()
//
//   // If the select picker already has a department selected when the page is loaded,
//   // then we want to populate the data table with the selected department
//   var departmentDropDown = $("#departmentDropDown");
//   var departmentSelected = $('option:selected', departmentDropDown).attr('value');
//   if (departmentSelected) {
//     populateTable()
//   }
// });

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
  // This function will take input from the department select picker, and based
  // off of what department is choosen, the function will populate both the data table
  // and the modal with the correct data from that department

  // This grabs the department selected from the select picker
  var departmentDropDown = $("#departmentDropDown");
  var departmentSelected = $('option:selected', departmentDropDown).attr('value');

  // AJAX call sends our controller the department choosen, and the controller
  // should send back the data we need as JSON
  $.ajax({
    method: "GET",
    url: "/main/department/selection/" + departmentSelected,
    datatype: "json",
    success: function(response) {

      // This section checks to see which button is currently pressed, and filters
      // the data table based off that button so that the data is filtered correctly
      // when we append the new data into the data table.
      // Before we append the new department data into the data table, this section will
      // first delete all of the current department data that we have in the data table.
      if ($("#currentDepartmentStudents").hasClass('btn-primary')){
        table
        .columns( 1 )
        .search("All Department Students")
        .draw();
        table
        .rows({ filter : 'applied'}).remove().draw();

        table
        .columns( 1 )
        .search("Current Department Students")
        .draw();
        table
        .rows({ filter : 'applied'}).remove().draw();
      }
      else{
        table
        .columns( 1 )
        .search("Current Department Students")
        .draw();
        table
        .rows({ filter : 'applied'}).remove().draw();

        table
        .columns( 1 )
        .search("All Department Students")
        .draw();
        table
        .rows({ filter : 'applied'}).remove().draw();
      }

      // This section will clear any data currently in the Div's because we will
      // be repopulating them with new department data
      $("#currentDepartmentStudentsDiv").empty()
      $("#allDepartmentStudentsDiv").empty()

      // Parse the JSON we get back from the controller
      response = JSON.parse(response)
      // This section will iterate through the JSON data, and access the values
      // from the key-value pairs that we will need to populate both the modal and the
      // data table
      for (var key in response){
        var bNumber = response[key]["BNumber"]
        var student = response[key]["Student"]
        var term = response[key]["Term"]
        var position = response[key]["Position"]
        var department = response[key]["Department"]
        var status = response[key]["Status"]
        var divClass = response[key]["checkboxModalClass"]
        var formID = response[key]["formID"]
        var activeStatus = response[key]["activeStatus"]
        var formStatus = response[key]["formStatus"]

        // The first "If" statment will populate both the data table and modal if the student's activeStatus == 'True', meaning that the
        // student is currently still a student at Berea
        if (activeStatus == "True") {
          table.row.add(["<a href='/laborHistory/" + departmentSelected + '/' + bNumber + "'value=0>" + "<span class='h4'>" + student + " (" + bNumber + ")" + "</a>"
          + "<span class='pushRight h5'>" + formStatus + "</span>" + "<br />"+ "<span class='pushLeft h6'>" + term + " - " + position + " - " + department + "</span>",
          "<span style='display:none'>" + status + "</span>"])
          .draw()

          if (divClass == "currentDepartmentModal"){
            $("#currentDepartmentStudentsDiv").append('<label class="container"><input class="' + divClass + '"type="checkbox" name="' + formID + '" id="' + formID +'" value="' + formID +'"/>' + student +'</label><br/>')
          }
          else{
            $("#allDepartmentStudentsDiv").append('<label class="container"><input class="' + divClass + '"type="checkbox" name="' + formID + '" id="' + formID +'" value="' + formID +'"/>' + student +'</label><br/>')
          }
        }
        // The "Else" statment will populate both the data table and modal if the student's activeStatus == 'False', meaning that the
        // student is no longer a student at Berea
        else{
          table.row.add(["<a href='/laborHistory/" + departmentSelected + '/' + bNumber + "'value=0>" + "<span class='h4'>" + student + " (" + bNumber + ")" + "</a>" +
          "<br />" + "<span class='pushLeft h6'>No longer a student.</span>",
          "<span style='display:none'>" + status + "</span>"])
          .draw()

          $("#allDepartmentStudentsDiv").append('<label class="container"><input class="' + divClass + '"type="checkbox" name="' + formID + '" id="' + formID +'" value="' + formID +'"/>' + student +' <strong>(No longer a student.)</strong></label><br/>')
        }

      }
    }
  })
}
