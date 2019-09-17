
function insertApprovals() {
  var labor_details_ids = [];
  var getChecked = $('input:checked').each(function() {
    labor_details_ids.push(this.value);
  })
  // $("#StudentId").text(labor_details_ids);
  data = JSON.stringify(labor_details_ids);
 $.ajax({
   type: "POST",
   url: "/admin/checkedForms",
   datatype: "json",
   data: data,
   contentType: 'application/json',
   success: function(response){
     if (response){
       // console.log(response);
       returned_details = response;
        $("#approvalModal").empty().append(returned_details);
       updateApproveTableData(returned_details);
      }
    }
  })
};
//this method adds data to each row in the approve selected Modal
function updateApproveTableData(returned_details){
  for (var i = 0; i < returned_details.length; i++){
    var student=returned_details[i][0]
    var position= returned_details[i][1]
     var hour= returned_details[i][2]
      var supervisor= returned_details[i][3]
      $('#classTable').append('<tr><td>'+student+'</td><td>'+position+'</td><td> '+supervisor+'</td> <td> '+hour+'</td></tr>');
       // $("#approvalModal").empty().append(returned_details);
  }

}

function getNotes (formID) {
  console.log(formID);

  $.ajax({
    type: "GET",
    url: "/admin/getNotes/"+formID,
    datatype: "json",
    success: function (response) {
      if (!("Success" in response)) {
        console.log(response);
        console.log(response["supervisorNotes"])
        // var testingText = document.createTextNode("This is a test for the p tag")

        console.log($("#notesText").html(response["supervisorNotes"]));
        $("#notesText").html(response["supervisorNotes"]);

      } else {
            $("#notesText").empty();
            }
    }
  })
};



function saveLaborNotes() { // saves notes written in textarea when save button of modal is clicked
  var notesTextId = $("#dummyInput").val();
  var notesUniqueId = "notes_" + notesTextId;
  console.log(notesUniqueId);
  document.getElementById("laborNotesText").value=document.getElementById(notesUniqueId).getAttribute("data-note");
  document.getElementById("saveNotes").setAttribute('onclick',"saveNotes('" + notesUniqueId +"')");
  console.log(idDummyInput);
}

 function saveNotes() { // saves notes written in textarea when save button of modal is clicked
   var notes = document.getElementById("laborNotesText").value;
   document.getElementById(notesTextId).setAttribute("data-note", notes);
 }

 function notesInsert() {
   notes = []
   data = JSON.stringify(notes);
   $("#saveNotes").on('submit', function(e) {
     e.preventDefault();
     });


   $.ajax({
          method: "POST",
          url: '/laborstatusform/notesInsert',
          data: notes,
          contentType: 'application/json',
          success: function(response) {
            console.log(response);

          }
        });
}

function createTabledataDictionary() { // puts all of the forms into dictionaries
  var listDictAJAX = [];
  $('#mytable tr').has('td').each(function() {
    /* Get the input box values first */
      supervisor = $("#selectedSupervisor").val();
      department = $("#selectedDepartment").val();
      term = $("#selectedTerm").val();
      var whichTerm = term.toString().substr(-2);
      startDate = $("#dateTimePicker1").val();
      endDate = $("#dateTimePicker2").val();
      var positionCode = $("#position_code").attr("data-posn");
      listDict = []
      listDict.push(supervisor, department, term, startDate, endDate, positionCode)
      var headersLabel = ["Supervisor", "Department", "Term", "Start Date", "End Date", "Position Code"]
      var tableDataDict = {};
      for (i in listDict) {
        tableDataDict[headersLabel[i]] = listDict[i];
      }

      /* If it's a break, get table values */
      if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00) {
        tableDataDict["Job Type"] = "Secondary";
        var headers_2_data = ["Student", "Position", "Contract Hours"];
        $('td', $(this)).each(function(index, item) {
          var aTag = $.parseHTML($(item).html());
          if (!$(aTag).hasClass('remove')) {
            var notes = $(aTag).data('note');
            tableDataDict["Supervisor Notes"] = notes;
            tableDataDict[headers_2_data[index]] = $(item).html();
          }
        });
        listDictAJAX.push(tableDataDict);
        allTableDataDict = {}
        for ( var key in listDictAJAX){
          allTableDataDict[key] = listDictAJAX[key];
        }
      }
      /* If it's academic year, get the table values */
      else {
          var headersData = ["Student", "Position", "Job Type", "Hours Per Week"];
          $('td', $(this)).each(function(index, item) {
            var aTag = $.parseHTML($(item).html());
            if (!$(aTag).hasClass('remove')) {
              var notes = $(aTag).data('note');
              tableDataDict["Supervisor Notes"] = notes;
              tableDataDict[headersData[index]] = $(item).html();
            }
          });
          listDictAJAX.push(tableDataDict);
          allTableDataDict = {} // this is the dictionary that contains all the forms
          for ( var key in listDictAJAX){
            allTableDataDict[key] = listDictAJAX[key];
          }
      }
     });

  delete allTableDataDict["0"] // gets rid of the first dictionary that contains table labels
  return allTableDataDict
}

function approve_selected(){
  ss = $("#student").text();
  console.log(ss);
}

// SEND DATA TO THE DATABASE
// function approvalInsert(){
//   var allTableDataDict = createTabledataDictionary()
//   data = JSON.stringify(allTableDataDict);
//   $('#laborStatusForm').on('submit', function(e) {
//     e.preventDefault();
//   });
//   $.ajax({
//          method: "POST",
//          url: '/laborstatusform/approvalInsert',
//          data: data,
//          contentType: 'application/json',
//          success: function(response) {
//            term = $("#selectedTerm").val();
//            var whichTerm = term.toString().substr(-2);
//            modalList = [];
//            if (response){
//              for (var key in allTableDataDict) {
//                var student = allTableDataDict[key]["Student"];
//                var position = allTableDataDict[key]["Position"];
//                var selectedContractHours = allTableDataDict[key]["Contract Hours"];
//                var jobType = allTableDataDict[key]["Job Type"];
//                var hours = allTableDataDict[key]["Hours Per Week"];
//                if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
//                  var bigString = "<li>" +"<span class='glyphicon glyphicon-ok' style='color:green'></span> " + student + ' | ' + position + ' | ' + selectedContractHours;
//                }
//                else {
//                  var bigString = "<li>"+"<span class='glyphicon glyphicon-ok' style='color:green'></span> " + student + ' | ' + position + ' | ' + jobType + ' | ' + hours;
//               }
//               modalList.push(bigString)
//             }
//           }
//
//           else {
//             for (var key in allTableDataDict) {
//                var student = allTableDataDict[key]["Student"];
//                var position = allTableDataDict[key]["Position"];
//                var selectedContractHours = allTableDataDict[key]["Contract Hours"];
//                var hours = allTableDataDict[key]["Hours Per Week"];
//
//               if (whichTerm != 11 && whichTerm !=12 && whichTerm !=00){
//                var bigString = "<li>" +"<span class='glyphicon glyphicon-remove' style='color:red'></span> " + student + ' | ' + position + ' | ' + selectedContractHours;
//               }
//               else {
//                 var bigString = "<li>"+"<span class='glyphicon glyphicon-remove' style='color:red'></span> " + student + ' | ' + position + ' | ' + jobType + ' | ' + hours;
//               }
//               modalList.push(bigString)
//             }
//            }
//          document.getElementById("approvedModal").innerHTML = "Labor status form(s) was approved for:<br><br>" +
//                                                                  "<ul style='list-style-type:none; display: inline-block;text-align:left;'>" +
//                                                                  modalList.join("</li>")+"</ul>"
//          $('#SubmitModal').modal('show')
//        }
//      });
//
//       $('#exampleModal').modal({backdrop: true, keyboard: false, show: true});
//       $('#exampleModal').data('bs.modal').options.backdrop = 'static';
//       document.getElementById('validApprovalModal').innerHTML = "Done";
//      document.getElementById('validApprovalModal').onclick = function() { window.location.replace("/laborstatusform");}
// }
