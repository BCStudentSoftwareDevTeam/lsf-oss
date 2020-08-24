

$(document).ready(function(){
  $('.highlight').click(function(){
    $('a').removeClass("active");
    $(this).addClass("active");
  })
})
function checkBrowser() {
  // Get the user-agent string
  let userAgentString = navigator.userAgent;

  // Detect Chrome
  let chromeAgent = userAgentString.indexOf("Chrome") > -1;

  if (chromeAgent = true) {
    varTabIndex = "tabindex=0"
  } else {
    varTabIndex =
  }
