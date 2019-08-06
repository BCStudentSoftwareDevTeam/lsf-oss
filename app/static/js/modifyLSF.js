function date() {

}

var j = jQuery.noConflict();
  j( function() {
      j( "#datetimepicker0" ).datepicker();
  } );


$('.glyphicon-calendar').click(function() {
    $("#datetimepicker0").focus();
  });
