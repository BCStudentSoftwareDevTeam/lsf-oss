var j = jQuery.noConflict();
j( function() {
    j( "#datepicker0" ).datepicker();
} );

$('.glyphicon-calendar').click(function() {
   $("#datepicker0").focus();
 });

var date = new Date();
date.setDate(date.getDate()+1);
$("#datepicker0").datepicker({
  minDate: date
});
$("#datepicker0").datepicker("setDate", "date");

$(function() {
   $("#submit").click(function() {
    if($("#condition").val() == "" || $("#datepicker0").val() == "" || $("#reason").val() == "") {
      category = "danger"
      msg = "Please fill out all fields before submitting.";
      $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
      $("#flasher").delay(3000).fadeOut()
    }
    else {
      $("#modal").modal("show");
    }
   });
});
