// Opens collapse menu for this page
$("#admin").collapse("show");
$("#addLaborAdmin input").on("change", function(){
  console.log("Hello world");
})

function hello() {
  console.log("Hello funtion")
}

function modal(button) {
  if(button == "add" && $("#addlaborAdmin").val() != "") {
    $("h2").html("Labor Administrators");
    $("p").html("Are you sure you want to add " + $("#addlaborAdmin option:selected").text() + " as a Labor Administrator?");
    document.getElementById("submitModal").setAttribute("name", "add");
    document.getElementById("submitModal").setAttribute("value", "add");
    $("#modal").modal("show");
  }
  else if(button == "add1" && $("#addFinAidAdmin").val() != "") {
    $("h2").html("Financial Aid Administrators");
    $("p").html("Are you sure you want to add " + $("#addFinAidAdmin option:selected").text() + " as a Financial Aid Administrator?");
    document.getElementById("submitModal").setAttribute("name", "addAid");
    document.getElementById("submitModal").setAttribute("value", "addAid");
    $("#modal").modal("show");
  }
  else if(button == "add2" && $("#addSaasAdmin").val() != "") {
    $("h2").html("SAAS Administrators");
    $("p").html("Are you sure you want to add " + $("#addSaasAdmin option:selected").text() + " as a SAAS Administrator?");
    document.getElementById("submitModal").setAttribute("name", "addSaas");
    document.getElementById("submitModal").setAttribute("value", "addSaas");
    $("#modal").modal("show");
  }
  else if(button == "remove" && $("#removelaborAdmin").val() != "") {
    $("h2").html("Labor Administrators");
    $("p").html("Are you sure you want to remove " + $("#removelaborAdmin option:selected").text() + " as a Labor Administrator?");
    document.getElementById("submitModal").setAttribute("name", "remove");
    document.getElementById("submitModal").setAttribute("value", "remove");
    $("#modal").modal("show");
  }
  else if(button == "remove1" && $("#removeFinAidAdmin").val() != "") {
    $("h2").html("Financial Aid Administrators");
    $("p").html("Are you sure you want to remove " + $("#removeFinAidAdmin option:selected").text() + " as a Financial Aid Administrator?");
    document.getElementById("submitModal").setAttribute("name", "removeAid");
    document.getElementById("submitModal").setAttribute("value", "removeAid");
    $("#modal").modal("show");
  }
  else if(button == "remove2" && $("#removesSaasAdmin").val() != "") {
    $("h2").html("SAAS Administrators");
    $("p").html("Are you sure you want to remove " + $("#removeSaasAdmin option:selected").text() + " as a SAAS Administrator?");
    document.getElementById("submitModal").setAttribute("name", "removeSaas");
    document.getElementById("submitModal").setAttribute("value", "removeSaas");
    $("#modal").modal("show");
  }
  else {
    category = "danger"
    msg = "Please select a user.";
    $("#flash_container").prepend('<div class="alert alert-'+ category +'" role="alert" id="flasher">'+msg+'</div>')
    $("#flasher").delay(3000).fadeOut()
      }
};
