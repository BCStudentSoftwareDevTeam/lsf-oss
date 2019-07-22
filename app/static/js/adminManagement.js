$(document).ready(function() { console.log("Howdy") });
function modal(button) {
  if(button == "add" && $("#addlaborAdmin").val() != "") {
    document.getElementById("submitModal").setAttribute("name", "add");
    document.getElementById("submitModal").setAttribute("value", "add");
    $("#modal").modal("show");
  }
  else if(button == "add1" && $("#addFinAidAdmin").val() != "") {
    document.getElementById("submitModal").setAttribute("name", "addAid");
    document.getElementById("submitModal").setAttribute("value", "addAid");
    $("#modal").modal("show");
  }
  else if(button == "add2" && $("#addSaasAdmin").val() != "") {
    document.getElementById("submitModal").setAttribute("name", "addSaas");
    document.getElementById("submitModal").setAttribute("value", "addSaas");
    $("#modal").modal("show");
  }
  else if(button == "remove" && $("#removelaborAdmin").val() != "") {
    document.getElementById("submitModal").setAttribute("name", "remove");
    document.getElementById("submitModal").setAttribute("value", "remove");
    $("#modal").modal("show");
  }
  else if(button == "remove1" && $("#removeFinAidAdmin").val() != "") {
    document.getElementById("submitModal").setAttribute("name", "removeAid");
    document.getElementById("submitModal").setAttribute("value", "removeAid");
    $("#modal").modal("show");
  }
  else if(button == "remove2" && $("#removesSaasAdmin").val() != "") {
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



// $(function() {
//    $("#add").click(function() {
//     if($("#addlaborAdmin").val() == "") {
//       console.log($('#addlaborAdmin').val())
//       category = "danger"
//       msg = "Please select a user";
//       $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
//       $("#flasher").delay(3000).fadeOut()
//     }
//     else {
//       $("#modal").modal("show");
//     }
//    });
//   });
