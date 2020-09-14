$(document).ready(function(){
  // $('.highlight').click(function(){
  //   $('.navbar a').removeClass("active");
  //   $(this).addClass("active");
  // });
  let userAgentString = navigator.userAgent;
  // Detect Chrome

  let chromeAgent = userAgentString.indexOf("Chrome") > -1;
  if (chromeAgent == true ){
    $('.navbar a').removeAttr('tabindex');
    $('.navbar li').removeAttr('tabindex');
    $('.navbar div').removeAttr('tabindex');  }

  $('#sidebar a').each(function() {
    console.log(window.location.pathname.indexOf($(this).attr('href')));
    if ((window.location.pathname.indexOf($(this).attr('href'))) > -1){
        $(this).children(".panel-heading").addClass('active');
        console.log(this);
    }
    else {
      if ((window.location.pathname.indexOf($(this).attr('href'))) == -1){
          console.log(this);
    }}
});
})
$('.panel-heading').click(function(){
  $('.panel-heading ').removeClass('active');
  $(this).addClass('active');
});
