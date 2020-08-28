
$(document).ready(function(){
  console.log("debug001");
  // $('.highlight').click(function(){
  //   $('.navbar a').removeClass("active");
  //   $(this).addClass("active");
  // });
  let userAgentString = navigator.userAgent;
  // Detect Chrome

  let chromeAgent = userAgentString.indexOf("Chrome") > -1;
  console.log("Line21");
  console.log(chromeAgent);
  var num = true;
  if (num == true){
    $('.navbar a').removeAttr('tabindex');
    $('.navbar li').removeAttr('tabindex');
    $('.navbar div').removeAttr('tabindex');
  }
})

// Get all buttons with class="btn" inside the container
var all = document.getElementById("sidebar");
var links = all.getElementsByClassName("highlight");
// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < links.length; i++) {
    links[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    console.log("Trying to get the colors work 0000");
    if (current != null){
    current[0].className = current[0].className.replace("active", "");
    this.className += " active";
    console.log("Trying to get the colors work")
  }
  });
}
