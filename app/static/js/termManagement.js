$('.datepicker').datepicker()
   .on('changeDate', function(e) {
     alert($(this).data('startEnd'));
     console.log($(this).data('startEnd'));
   });

$('.glyphicon-calendar').click(function() {
   $(".datepicker").focus();
 });

var date = new Date();
date.setDate(date.getDate());
$(".form-control").datepicker({
});

function update_startDate(response, obj){
  console.log(response)
  console.log(obj)
  var selected_termStart = obj.value;
  document.getElementById(obj.id).value = selected_termStart
  console.log(selected_termStart)
}

function getDate(obj, termCode) {
  var termStart = obj.value; // This is the start date
  console.log(termStart)
  console.log(termCode)
  var list_dict_ajax = []
  var list_dict = []
  console.log($('#start').val())
  list_dict.push(termStart, termCode)
  var headers_label = ["start date", "termCode"]
  var tabledata_dict = {};
  for (i in list_dict) {
    tabledata_dict[headers_label[i]] = list_dict[i]
  }
  list_dict_ajax.shift();
  list_dict_ajax.push(tabledata_dict)
  test_dict = {}
  for (var key in list_dict_ajax){
    test_dict[key] = list_dict_ajax[key];
  }
  console.log(test_dict)
  data = JSON.stringify(test_dict);
  console.log(termCode)
  // $('#start').each(function() {
  //   startDate = $('#start').val()
  // })
  // console.log(termCode)
  // console.log(obj)           // This is the whole object that contains the id, value, etc.
  // console.log(termStart)
  // console.log("hi")
    $.ajax({
      type: "POST",
      url: "/termManagement/getDate/",
      datatype: "json",
      data: data,
      contentType: 'application/json',
      success: function(response){
        console.log("js success")
      }
    });
}


// $.ajax({
//   type: "POST",
//   url:"/termManagement" +
// })
// var acc = document.getElementsByClassName("accordion");
// var i;
//
// for (i = 0; i < acc.length; i++) {
//  acc[i].addEventListener("click", function() {
//    this.classList.toggle("active");
//    var panel = this.nextElementSibling;
//    if (panel.style.display === "block") {
//      panel.style.display = "none";
//    } else {
//      panel.style.display = "block";
//    }
//  });
// }
