
function insertApprovals() {
  var ids = [];
  var getChecked = $('input:checked').each(function() {
    ids.push(this.value);
    console.log(ids);
  })
  data = JSON.stringify(ids);

 $.ajax({
   type: "POST",
   url: "/admin/checkedForms",
   datatype: "json",
   data: data,
   contentType: 'application/json',
   success: function(response){
     if (response){
       console.log(response);

   }
 }
 })
};
