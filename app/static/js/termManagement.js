var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
 acc[i].addEventListener("click", function() {
   this.classList.toggle("active");
   var panel = this.nextElementSibling;
   if (panel.style.display === "block") {
     panel.style.display = "none";
   } else {
     panel.style.display = "block";
   }
 });
}

$('.datepicker').datepicker()
   .on('changeDate', function(e) {
     alert($(this).data('startEnd'));
     console.log($(this).data('startEnd'));
   });

$('.glyphicon-calendar').click(function() {
   $(".datepicker").focus();
 });

var date = new Date();
date.setDate(date.getDate());
$(".form-control").datepicker({
});


function getDate(obj, termCode) {

  var termStart = obj.value; // This is the start date
  var termID = obj.id.split("_")[1] //
  var dateType = obj.id.split("_")[0]
  var tabledata_dict = {};
  tabledata_dict[dateType] = obj.value;
  tabledata_dict["termCode"] = termID;
  data = JSON.stringify(tabledata_dict);
  console.log(data)
    $.ajax({
      type: "POST",
      url: "/termManagement/setDate/",
      datatype: "json",
      data: data,
      contentType: 'application/json',
      success: function(response){
        console.log("js success")
      }
    });
}
