/*$(document).ready(function () {
    // Alert categories: https://getbootstrap.com/docs/4.0/components/alerts/
    category = "danger";
    msg = "An example flash message generated using jquery";
    x = $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
})
*/

$(document).ready(function(){
  $('.highlight').click(function(){
    $('.highlight').removeClass("weird");
    $(this).addClass("weird");
  })
})
