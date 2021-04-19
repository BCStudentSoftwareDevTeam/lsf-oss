function submitChanges() {
  var learningObjectiveList = []
  $("#table_LearningObjective tr:gt(0)").each(function () {
        var this_row = $(this);
        var rowContent = $.trim(this_row.find('td:eq(0)').html());
        learningObjectiveList.push(rowContent)
    });
  var qualificationList = []
  $("#table_Qualification tr:gt(0)").each(function () {
        var this_row = $(this);
        var rowContent = $.trim(this_row.find('td:eq(0)').html());
        qualificationList.push(rowContent)
    });
  var dutyList = []
  $("#table_Duty tr:gt(0)").each(function () {
        var this_row = $(this);
        var rowContent = $.trim(this_row.find('td:eq(0)').html());
        dutyList.push(rowContent)
    });
  var positionTitle = $("#positionTitle").html();
  var positionCode = positionTitle.slice(-6);
  var data = {"learningObjective": learningObjectiveList,
              "qualification": qualificationList,
              "duties": dutyList,
              "positionCode": positionCode}
  data = JSON.stringify(data)
  $.ajax({
    type: "POST",
    url: "/positionDescriptionEdit/submitRevisions",
    data: data,
    contentType: 'application/json',
    success: function (response){
      // Need to put all of the text into the textarea now
      console.log("Made it back here");
      console.log(response);
     }
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

function saveChanges() {
  $("#header").html('<h2 class="modal-title" style="text-align:center" id="title">Submit Revision</h2>')
  $("#body").html("<p style='text-align:center'>Requesting an edit will not result in an immediate change. " +
                  "A labor admin will need to review your edit, and you will be " +
                  "notified via email if it was approved or denied.</p>" +
                  "<p style='text-align:center'><strong>If your revision is approved, the current position " +
                  "description will be archived and the new position description " +
                  "will be applied to all future labor status forms with the revised description." +
                  "</strong></p>")
  $("#footer").html('<button type="button" class="btn btn-danger" data-dismiss="modal" style="float:left">Close</button>' +
                    '<button class="btn btn-success" id="submitModal" onclick="submitChanges()">Submit Revision</button>')
  $("#modal").modal("show");
}

function adminApprove() {
  $("#header").html('<h2 class="modal-title" style="text-align:center" id="title"></h2>')
  $("#body").html("<p style='text-align:center'>You are approving</p>" +
                  "<p style='text-align:center'><strong>If your revision is approved, the current position " +
                  "description will be archived and the new position description " +
                  "will be applied to all future labor status forms with the revised description." +
                  "</strong></p>")
  $("#footer").html('<button type="button" class="btn btn-danger" data-dismiss="modal" style="float:left">Close</button>' +
                    '<button class="btn btn-success" id="submitModal" onclick="beginEdit()">Submit Supervisor</button>')
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
