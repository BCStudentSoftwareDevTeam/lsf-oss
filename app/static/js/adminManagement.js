// function fillAdmin(response) {
//   var adminselect = document.getElementbyID("add")
//     $("#add").empty();
//     var count = 0
//     for (var key in response){
//         count = count + 1;
//         var option = document.createElement("option");
//           option.text=response[key]["FIRST_NAME"].toString+" "+response[key]["LAST_NAME"].toString()+" ("+ response[key]["username"].toString() + ")";
//           option.value = key;
//           adminselect.appendChild(option);
//     }
//     if (count < 2) {
//       var disable_btn = document.getElementById("adminbtn");
//       disable_btn.disabled = true;
//     }
//   $('.selectpicker').selectpicker('refresh');
// }
//
// function retrieveAdmins() {
//   $ajax({
//     datType : "json",
//     url:"/admin/adminManagement/get_admin",
//     type:"GET"
//     success:function(response)
//     fillAdmin(response);
//   })
// }
