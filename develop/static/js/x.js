$(function() {
    $('#ajax1').click(function () {
    var data = {
         data: JSON.stringify({"lesson": "Operation System", "score": 100})
   }
      $.ajax({
        url:"/sendjson",
        type: 'POST',
        data: data,
        success: function (msg) {
            var html = "";
            html += "<span>" + msg.name + "</span>";
            $("#ajax2").html(html);
        }
    })
  })
})
//<script>
//    $(#ajax1).click(function () {
//    var data = {
//         data: JSON.stringify({"lesson": "Operation System", "score": 100})
//   }
//      $.ajax({
//        url:"/sendjson",
//        type: 'POST',
//        data: data,
//        success: function (msg) {
//            var html = "";
//            html += "<span>123: " + data.name + "</span>";
//            $("ajax1").html(html);
////            alert(msg.name)
//        }
//    })
//  });
//</script>