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
