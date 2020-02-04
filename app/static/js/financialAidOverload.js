var labor_details_ids = []; // for insertApprovals() and final_approval() only
function insertApprovals() {
  var getChecked = $('input:checked').each(function() {
    labor_details_ids.push(this.value);
    });

  //this checks wether the checkbox is checked or not and if does not it disable the approve selected button
  var atLeastOneIsChecked = $('input[name="check[]"]:checked').length > 0;
  if (!atLeastOneIsChecked){
    $("#approveSelected").prop("disabled",true);
    $("#approvePendingForm").prop("disabled",true);
    $("#modifiedApproval").prop("disabled",true);
    $("#approveOverload").prop("disabled",true);
    $("#approveRelease").prop("disabled",true);

     location.reload();
       }
    var data = JSON.stringify(labor_details_ids);
   $.ajax({
     type: "POST",
     url: "/admin/checkedForms",
     datatype: "json",
     data: data,
     contentType: 'application/json',
     success: function(response){
       if (response){
         var returned_details = response;
         updateApproveTableData(returned_details);
              }
            }
          });
      }
