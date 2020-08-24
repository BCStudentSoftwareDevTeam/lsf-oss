
$(document).ready(function(){
  console.log("debug001");
  // $('.highlight').click(function(){
  //   $('a').removeClass("active");
  //   $(this).addClass("active");
  // })
  let userAgentString = navigator.userAgent;
  // Detect Chrome

  let chromeAgent = userAgentString.indexOf("Chrome") > -1;
  console.log("Line21");
  console.log(chromeAgent);
  if (chromeAgent == true){
    $('a').removeAttr('tabindex');
    $('li').removeAttr('tabindex');
    $('div').removeAttr('tabindex');
  }
})
