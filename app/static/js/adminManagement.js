$(document).ready(function());
function modal(button) {
  if(button == "add" && $("#addlaborAdmin").val() != "") {
    $("p").html("Are you sure you want to add " + $("#addlaborAdmin option:selected").text() + " as an admin?");
    document.getElementById("submitModal").setAttribute("name", "add");
    document.getElementById("submitModal").setAttribute("value", "add");
    $("#modal").modal("show");
  }
  else if(button == "add1" && $("#addFinAidAdmin").val() != "") {
    $("p").html("Are you sure you want to add " + $("#addFinAidAdmin").val() + " as an admin?");
    document.getElementById("submitModal").setAttribute("name", "addAid");
    document.getElementById("submitModal").setAttribute("value", "addAid");
    $("#modal").modal("show");
  }
  else if(button == "add2" && $("#addSaasAdmin").val() != "") {
    $("p").html("Are you sure you want to add " + $("#addSaasAdmin").val() + " as an admin?");
    document.getElementById("submitModal").setAttribute("name", "addSaas");
    document.getElementById("submitModal").setAttribute("value", "addSaas");
    $("#modal").modal("show");
  }
  else if(button == "remove" && $("#removelaborAdmin").val() != "") {
    $("p").html("Are you sure you want to remove " + $("#removelaborAdmin").val() + "?");
    document.getElementById("submitModal").setAttribute("name", "remove");
    document.getElementById("submitModal").setAttribute("value", "remove");
    $("#modal").modal("show");
  }
  else if(button == "remove1" && $("#removeFinAidAdmin").val() != "") {
    $("p").html("Are you sure you want to remove " + $("#removeFinAidAdmin").val() + "?");
    document.getElementById("submitModal").setAttribute("name", "removeAid");
    document.getElementById("submitModal").setAttribute("value", "removeAid");
    $("#modal").modal("show");
  }
  else if(button == "remove2" && $("#removesSaasAdmin").val() != "") {
    $("p").html("Are you sure you want to remove " + $("#removeSaasAdmin").val() + "?");
    document.getElementById("submitModal").setAttribute("name", "removeSaas");
    document.getElementById("submitModal").setAttribute("value", "removeSaas");
    $("#modal").modal("show");
  }
  else {
    category = "danger"
    msg = "Please select a user";
    $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
    $("#flasher").delay(3000).fadeOut()
}
};
