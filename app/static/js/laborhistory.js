$("#print").click(function fillPDF(){
  //alert("Hi")
  var doc = new jsPDF();
  doc.setTextColor(43, 66, 99);
  doc.setFontType("bold");
  doc.setFontSize(15);
  doc.text(20, 70, 'STATUS FORM')
  doc.text(20, 80, "Labor Position Participation Agreement");
  doc.setFontSize(9);
  doc.setFontType("normal");
  var loremipsum =  "The purpose of this form is to establish student work status during an academic term (Fall, Spring, or Summer), during a break period (Thanksgiving, Christmas, Spring Break), or for a summer practicume assginment."
  lines = doc.splitTextToSize(loremipsum, 170);
  doc.text(20, 90, lines);
  doc.setFontSize(15);
  doc.setFontType("bold");
  doc.text(20, 120, "Primary Contract");
  doc.setFontSize(15);
  doc.text(20, 170, "Guildlines");
  doc.setFontType("normal");
  doc.setFontSize(10);
  doc.text(20, 180, "Primary: ");
  var primText = " Positions through which a student meets the primary labor requirement during an academic term or working a summer practicum assignment. All students sign a Labor Enrollment Agreement upon admission to Berea College. In signing this form, each student agrees to"
  lines_2 = doc.splitTextToSize(primText, 170);
  doc.text(20, 185, lines_2);

  var primList_1 = "work no less than 10 hours a week and adhere to the work schedule as required by this position and arranged with the supervisor"
  var primList_2 = "work any additional hours as defined in this status form including adhering to the work schedule as required by the position"
  var primList_3= "secure approval for working continuously more than 15 hours per week as specified in the Labor overload approval process"


  doc.fromHTML("<ul><li>"+ primList_1+ "</li></ul>", 20, 200, {'width':180});
  doc.fromHTML("<ul><li>"+ primList_2+"</li></ul>", 20, 210, {'width':180});
  doc.fromHTML("<ul><li>"+ primList_3+"</li></ul>", 20,220, {'width':180});

  doc.setFontSize(10);
  doc.text(20, 230, "Secondary: ");
  var seconText = "Positon taken by a student in addition to his/her primary position. Students may take secondary jobs as a means of earning extra income, learning a new skill, participating in a desired program, or providing an important service. Primary supervisors must approve secondary positions and they may not interfere with the student's primary performance."
  lines_6 = doc.splitTextToSize(seconText, 170);
  doc.text(20, 235, lines_6);

  doc.setFontSize(10);
  doc.setFontType("bold");
  doc.text(20, 255, "SUPERVISOR CHECKLIST:");

  doc.fromHTML("<ul><li>Coffee</li><li>Tea</li><li>Milk</li></ul>",  20, 260);
  //  doc.output("dataurlnewwindow");


  doc.save();
  //doc.autoPrint()

});

function openModal(laborStatusKey) {
  /*
    This function gets a response from the controller function: populateModal() in laborHistory.py.  The response is the data for the modal that pops up
    when the position is clicked.
  */
  $.ajax({
    type: "GET",
    url: '/laborHistory/modal/' + laborStatusKey,
    success: function(response) {
      alert(response);
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
