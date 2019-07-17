$(document).ready(function () {
    category = "error";
    msg = "An example flash message generated using jquery";
    x = $("#flash_container").prepend('<div class="alert alert-info '+ category +' role="alert" id="flasher">'+msg+'</div>')
})
