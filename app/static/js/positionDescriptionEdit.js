$(window).load(function(){
  var wls = $("#buttonWLS").val();
  if (wls == "1") {
    $("#bodyWLS").html('<div class="floatleft"><ul><li><strong>Entry Level: WLS 1</strong></li>' +
                        '<li>Unskilled work</li>'+
                        '<li>Under supervision or structure</li>' +
                        '<li>Repetitive or routine in training</li>' +
                        '</ul></div>' +
                        '<div class="floatright"><ul><li><strong>Basic Work Habits and Attitudes</strong></li>' +
                        '<li>Meeting schedules</li>'+
                        '<li>Meeting standards of performance</li>' +
                        '<li>Efficient use of time</li>' +
                        '<li>Healthy attitudes toward work and supervision</li>' +
                        '<li>Working with others</li>' +
                        '<li>Sharing responsibility</li>' +
                        '<li>Recognition of importance of work</li>' +
                        '<li>Learning basic skills and information</li>' +
                        '</ul></div>');
  }
  else if (wls === "2") {
    $("#bodyWLS").html('<div class="floatleft"><ul><li><strong>Intermediate Level : WLS 2</strong></li>' +
                        '<li>Semi-skilled work</li>'+
                        '<li>Less direct supervision</li>' +
                        '<li>Some independent judgment</li>' +
                        '<li>Semi- independent knowledge of position</li>' +
                        '<li>Some work variety</li>' +
                        '</ul></div>' +
                        '<div class="floatright"><ul><li><strong>Responsibility and Skill Development</strong></li>' +
                        '<li>Taking personal responsibility</li>'+
                        '<li>Application of knowledge to situation</li>' +
                        '<li>Self-identification of skills, talents, interests, and limitations</li>' +
                        '<li>Learning and developing confidence in skills</li>' +
                        '<li>	Appreciation of work as a process as well as in terms of product</li>' +
                        '</ul></div>');
  }
  else if (wls === "3") {
    $("#bodyWLS").html('<div class="floatleft"><ul><li><strong>Skilled Level: WLS 3</strong></li>' +
                        '<li>Skilled work</li>'+
                        '<li>Little direct supervision</li>' +
                        '<li>Independent judgment of procedures</li>' +
                        '<li>Variety and depth</li>' +
                        '<li>Contributes to improvement</li>' +
                        '</ul></div>' +
                        '<div class="floatright"><ul><li><strong>Responsibility and Skill Development</strong></li>' +
                        '<li>Importance of initiative</li>'+
                        '<li>Awareness of needs</li>' +
                        '<li>Problem identification</li>' +
                        '<li>Analytical ability</li>' +
                        '<li>Problem solving</li>' +
                        '<li>Role of standards and leadership</li>' +
                        '</ul></div>');
  }
  else if (wls === "4") {
    $("#bodyWLS").html('<div class="floatleft"><ul><li><strong>Advanced Level: WLS 4</strong></li>' +
                        '<li>Program or skill competence at senior level</li>'+
                        '<li>Only general supervision received</li>' +
                        '<li>Either provides supervision to others or exercises other skills and judgment</li>' +
                        '</ul></div>' +
                        '<div class="floatright"><ul><li><strong>Understanding and Commitment</strong></li>' +
                        '<li>Understanding relationships between individuals, institutions, and processes</li>'+
                        '<li>Comprehension of values, realities, and goals</li>' +
                        '<li>Ability to articulate and interpret observations, experiences, and understanding</li>' +
                        '<li>Commitment to service essential to the department</li>' +
                        '</ul></div>');
  }
  else if (wls === "5") {
    $("#bodyWLS").html('<div class="floatleft"><ul><li><strong>Management Level: WLS 5</strong></li>' +
                        '<li>Senior-level autonomy</li>'+
                        '<li>Makes independent judgments on application of Policy</li>' +
                        '<li>Accepts management responsibility</li>' +
                        '<li>High technical or skill training</li>' +
                        '</ul></div>' +
                        '<div class="floatright"><ul><li><strong>Supervision and Management</strong></li>' +
                        '<li>Understanding of departmental management</li>'+
                        '<li>Taking responsibility for the effectiveness of others</li>' +
                        '<li>Awareness of departmental and institutional relationships</li>' +
                        '<li>Teaching and instruction techniques</li>' +
                        '<li>Communication and interpersonal skills</li>' +
                        '<li>Evaluation of workers and procedures</li>' +
                        '</ul></div>');
  }
  else if (wls === "6") {
    $("#bodyWLS").html('<div class="floatleft"><ul><li><strong>Director Level: WLS 6</strong></li>' +
                        '<li>Assumes program directing role</li>'+
                        '<li>Significant management responsibility</li>' +
                        '<li>Substantial supervisory responsibility</li>' +
                        '<li>Responsible for planning, training, and instruction</li>' +
                        '<li>Serves as role model for Berea community</li>' +
                        '</ul></div>' +
                        '<div class="floatright"><ul><li><strong>Leadership and Autonomy</strong></li>' +
                        '<li>Understanding of leadership in community context</li>'+
                        '<li>Development of responsible autonomy</li>' +
                        '<li>Ability to transmit values and interpretations to others</li>' +
                        '<li>Confidence of self-knowledge and value commitments</li>' +
                        '<li>Living the values of Bereas commitments</li>' +
                        '<li>High degree of independence</li>' +
                        '</ul></div>');
  }
  $("#headerWLS").html('<h2 class="modal-title" style="text-align:center" id="title">WLS (' + wls + ') Requirements</h2>');
  $("#footerWLS").html('<button type="button" class="btn btn-danger" data-dismiss="modal" style="float:center">Close</button>')
  $('#WLSModal').modal('show');
});

function grabTableDate() {
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
  combinedList = [learningObjectiveList, qualificationList, dutyList]
  return (combinedList)
}

function submitChanges() {
  tableContent = grabTableDate()
  var positionTitle = $("#positionTitle").html();
  var positionCode = positionTitle.slice(-6);
  var data = {"learningObjectives": tableContent[0],
              "qualifications": tableContent[1],
              "duties": tableContent[2],
              "positionCode": positionCode}
  data = JSON.stringify(data)
  $.ajax({
    type: "POST",
    url: "/positionDescriptionEdit/submitRevisions",
    data: data,
    contentType: 'application/json',
    success: function(response){
      window.location.replace("/positionDescriptions");
    }
  })
}

var recordID
function adminUpdate() {
  var adminChoice = $("#submitModal").val()
  if (adminChoice == "Deny") {
    var data = {"adminChoice": adminChoice,
                "recordID": recordID}
  }
  else if (adminChoice == "Approve") {
    tableContent = grabTableDate()
    var data = {"learningObjectives": tableContent[0],
                "qualifications": tableContent[1],
                "duties": tableContent[2],
                "recordID": recordID,
                "adminChoice": adminChoice}
  }
  data = JSON.stringify(data)
  $.ajax({
    type: "POST",
    url: "/positionDescriptionEdit/adminUpdate",
    data: data,
    contentType: 'application/json',
    success: function(response){
      console.log("Made it back")
      window.location.replace("/admin/viewPositionDescriptions");
    }
  })
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

function adminApprove(ID) {
  recordID = ID
  $("#header").html('<h2 class="modal-title" style="text-align:center" id="title">Approve Position Description</h2>');
  $("#body").html("<p style='text-align:center'>You are approving</p>" +
                  "<p style='text-align:center'><strong>If your revision is approved, the current position " +
                  "description will be archived and the new position description " +
                  "will be applied to all future labor status forms with the revised description." +
                  "</strong></p>");
  $("#footer").html('<button type="button" class="btn btn-danger" data-dismiss="modal" style="float:left">Close</button>' +
                    '<button class="btn btn-success" id="submitModal" value="Approve" onclick="adminUpdate()">Submit Supervisor</button>');
  $("#modal").modal("show");
}

function adminDeny(ID) {
  recordID = ID
  $("#header").html('<h2 class="modal-title" style="text-align:center" id="title">Deny Position Description</h2>')
  $("#body").html("<p style='text-align:center'>Are you sure you want to <strong>Deny</strong> " +
                  "this position description?</p>")
  $("#footer").html('<button type="button" class="btn btn-danger" data-dismiss="modal" style="float:left">Close</button>' +
                    '<button class="btn btn-success" id="submitModal" value="Deny" onclick="adminUpdate()">Submit Supervisor</button>')
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
