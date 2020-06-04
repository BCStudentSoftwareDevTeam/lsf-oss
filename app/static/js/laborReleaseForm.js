var j = jQuery.noConflict();
j( function() {
    j("#datepicker0").datepicker({

    });
} );

// This function creates the map glyphicon
// on the select-picker
$('.glyphicon-calendar').click(function() {
   $("#datepicker0").focus();
 });

// This sets the min date you can choose on the
// date picker as tomorrows date
var date = new Date();
date.setDate(date.getDate()+1);
$("#datepicker0").datepicker({
  minDate: date
});

// This function checks to see if all the fields have been filled before
// rendering the submit modal. If the submit button is clicked before all
// fields are filled, then the user gets a message
$(function() {
   $("#submit").click(function() {
    if($("#condition").val() == "" || $("#datepicker0").val() == "" || $("#reason").val() == "") {
      category = "danger"
      msg = "Please make sure that Condition at Release, Release Date, and Reason for Release are filled out before submitting.";
      $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
      $("#flasher").delay(5000).fadeOut()
    }
    else {
      $("#modal").modal("show");
    }
   });
});
