function fillPDF(laborStatusKey){
  /* This function gets a response from controller function: ConvertToPDF() in laborHistory.py. The response is an HTML Template
     that is converted to pdf using jsPDF*/
  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/printPdf/' + laborStatusKey,
    success: function(response) {
      var doc = new jsPDF('portrait', 'pt', 'letter') // Create a new jsPDF document
      margins = {
       top: 40,
       bottom: 60,
       left: 40,
       width: 522
       };
      doc.setTextColor(0,90,133);
      doc.fromHTML(response, margins.left,margins.top, {width: margins.width}); // Change the HTML template to PDF
      doc.save();

    }
  });
}

function openModal(laborStatusKey) {
  /*
    This function gets a response from the controller function: populateModal() in laborHistory.py.  The response is the data for the modal that pops up
    when the position is clicked.
  */
  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/' + laborStatusKey,
    success: function(response) {
      $("#holdModal").empty().append(response);
      $("#modal").modal("show");
      $("#modify").attr("href", "/modifyLSF/" + laborStatusKey); // will go to the modifyLSF controller
      $("#rehire").attr("href", "/laborstatusform/" + laborStatusKey); // will go to the lsf controller
      $("#release").attr("href", "/laborReleaseForm/" + laborStatusKey); // will go to labor release form controller
    }
  });
}

function withdrawform(formID){
  /*
  This funciton gets a response from the controller function: updatestatus_post() in laborHistory.py.  It reloads the page when the forms from the
  database are deleted by the controller function.
  */
  formIdDict={}
  formIdDict["FormID"] = formID
  data = JSON.stringify(formIdDict);
  $.ajax({
         method: "POST",
         url: '/laborHistory/modal/updatestatus',
         data: data,
         contentType: 'application/json',
         success: function(response) {
             if (response["Success"]) {
               window.location.href = response["url"]
             }
           }
         });
       }
