


var labor_details_ids = []; // for insertApprovals() and final_approval() only
function insertApprovals() {
  var getChecked = $('input:checked').each(function() {
    labor_details_ids.push(this.value);
  })

  //this checks wether the checkbox is checked or not and if does not it disable the approve selected button
  var atLeastOneIsChecked = $('input[name="check[]"]:checked').length > 0;
  if (!atLeastOneIsChecked){
    $("#approveSelected").prop("disabled",true);
    location.reload();

       }

    data = JSON.stringify(labor_details_ids);
   $.ajax({
     type: "POST",
     url: "/admin/checkedForms",
     datatype: "json",
     data: data,
     contentType: 'application/json',
     success: function(response){
       if (response){
         returned_details = response;
         updateApproveTableData(returned_details);
         // updateDenialTableData(returned_details);
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


  }

}

//this method changes the status of the lsf from pending to approved status
function finalApproval() {
  data = JSON.stringify(labor_details_ids);
  $.ajax({
    type: "POST",
    url: "/admin/finalApproval",
    datatype: "json",
    data: data,
    contentType: 'application/json',
    success: function(response){
      if (response){
        console.log('success', response["success"]);
        if(response["success"]) {
            console.log("It was true")
            location.reload(true);
        }
       }
     }
   })

 };


labor_denial_id=[];
function insertDenial(){
  //this checks wether the checkbox is checked or not and if does not it disable the approve selected button
  var getChecked = $('input:checked').each(function() {
    labor_denial_id.push(this.value);
  })
  console.log("denial id(s): ", labor_denial_id)

    data = JSON.stringify(labor_denial_id);
    console.log("data :", data)
   $.ajax({
     type: "POST",
     url: "/admin/checkedForms",
     datatype: "json",
     data: data,
     contentType: 'application/json',
     success: function(response){
       if (response){
         console.log("response: ", response);
         labor_denial_detials = response;
         finalDenial_data(labor_denial_detials);
         // updateDenialTableData(returned_details);
        }
      }
    })
};


function finalDenial_data(returned_details){
  for (var i = 0; i < returned_details.length; i++){
    var student=returned_details[i][0]
    var position= returned_details[i][1]
     var hour= returned_details[i][2]
     var someHousrs= returned_details[i][3]
      var supervisor= returned_details[i][4]
      console.log("hour ", hour)
      $('#denyTable').append('<tr><td>'+student+'</td><td>'+position+'</td><td> '+supervisor+'</td> <td> '+hour+'</td></tr>');


  }

}


//this function is for final approve button in the approve selected modal
// function finalApproval() {
//   data = JSON.stringify(labor_details_ids);
//   console.log("before ajax call ")



 function finalDenial() {
   data = JSON.stringify(labor_details_ids);
   $.ajax({
     type: "POST",
     url: "/admin/finalDenial",
     datatype: "json",
     data: data,
     contentType: 'application/json',
     success: function(response){
       if (response){
         console.log('success', response["success"]);
         if(response["success"]) {
             console.log("It was true")
             location.reload(true);
         }
        }
      }
    })

  };








// this refreshes the page each time form(s) is approved to empty up the modal content
// $('#refreshContent').click(function() {
//     location.reload();
// });



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
