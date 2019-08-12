$(document).ready(function() {
  // When the page first loads, this function will make sure the data table is
  // only showing the correct buttons and data
  table
    .columns( 8 )
    .search("My Current Students")
    .draw();
  //
  // $("#currentDepartmentStudents").hide()
  // $("#allDepartmentStudents").hide()
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
  // $("#myCurrentStudents").removeClass("btn-primary");
  // $("#myCurrentStudents").addClass("btn-light");

});

var data = {
    'Pending Labor Status Forms': {
        col: ["contactid", "fullname", "age", "salary", "job"],
        row: [
            ["111", "Ryan Adams", 28, 750, "Accountant"],
            ["10", "Julie Connolly", 35, 800, "Programmer"]
        ]
    },
    'Pending Release Forms': {
        col: ['id', 'name', 'dateofbirth', 'grade1', 'grade2', 'grade3'],
        row: [
            ["45", "James Smith", "31/05/1984", 16, 17, 11],
            ["23", "Anne Newton", "25/03/1988", 15, 12, 18]
        ]
    }
};

$(document).ready(function() {

    var tabs = $('<div />').attr('id', 'tabs').appendTo('body');
    var listOfTabNames = $('<ul />').attr('id', 'tabNames').appendTo(tabs);

    for (var i in data) {
        var name = i;
        var idOfContentElement = 'tabContent-' + name;
        $('<li id="tabHeader-' + name + '"><a href="#' + idOfContentElement + '">' + name + '</a></li>').appendTo(listOfTabNames);
        var tabContent = $('<div />').attr('id', idOfContentElement).appendTo(tabs);

        var colData = data[i].col;
        var rowData = data[i].row;

        var table = $('<table/>').attr("id", "table-" + name)
                .addClass("display")
                .attr("cellspacing", "0")
                .attr("width", "100%")
                .appendTo(tabContent)
                ;

        var tr = $('<tr />');
        table.append('<thead>').children('thead').append(tr);

        for (var i = 0; i < colData.length; i++) {
            tr.append('<th>' + colData[i] + '</th>');
        }

        for(var r = 0; r < rowData.length; r++) {
            var tr = $('<tr />');
            table.append(tr);
            //loop through cols for each row...
            for(var c=0; c < colData.length; c++) {
                tr.append('<td>' + rowData[r][c] + '</td>');
            }
        }

        $("#tabContent").append(table);

        $("#table-" + name).DataTable({
            responsive: true
        });
    }

    $('#tabs').tabs();
});
