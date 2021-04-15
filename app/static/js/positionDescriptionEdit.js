function submitChanges() {
  $("#table_LearningObjective tr:gt(0)").each(function () {
        var this_row = $(this);
        var productId = $.trim(this_row.find('td:eq(0)').html());
        console.log(productId)
    });
  $("#table_Qualification tr:gt(0)").each(function () {
        var this_row = $(this);
        var productId = $.trim(this_row.find('td:eq(0)').html());
        console.log(productId)
    });
  $("#table_Duty tr:gt(0)").each(function () {
        var this_row = $(this);
        var productId = $.trim(this_row.find('td:eq(0)').html());
        console.log(productId)
    });
}

function addRow(button) {
  var parentTableID = button.parentNode.parentNode.id;
  var tableID = "#table_" + parentTableID + " tr:last"
  $(tableID).after(
    '<tr><td class="col-md-10 pt-3-half" contenteditable="true"></td>' +
    '<td class="col-md-1 pt-3-half">' +
      '<span class="table-up">' +
        '<a href="#!" class="indigo-text">' +
          '<i class="glyphicon glyphicon-arrow-up" aria-hidden="true"></i>' +
        '</a>' +
      '</span>' +
      '<span class="table-down">' +
        '<a href="#!" class="indigo-text">' +
          '<i class="glyphicon glyphicon-arrow-down" aria-hidden="true"></i>' +
        '</a>' +
      '</span>' +
    '</td>' +
    '<td class="col-md-1">' +
      '<span class="table-remove">' +
        '<button type="button" class="btn btn-danger btn-rounded btn-sm my-0" onclick="deleteRow(this)">Remove</button>' +
      '</span></td></tr>');
}

function deleteRow(button) {
  $(button).parents("tr").remove();
}

function saveChanges(currentUser) {
  console.log("Modal function")
  console.log(currentUser)
  $("#modal").modal("show");
}

$(".collapse").on('click', '.table-up', function () {
  var row = $(this).parents('tr');
  if(row.index() === 0) {
     return;
  }
  row.prev().before(row.get(0));
});

$(".collapse").on('click','.table-down', function () {
  var row = $(this).parents('tr');
  row.next().after(row.get(0));
});
