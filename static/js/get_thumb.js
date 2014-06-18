$('body').on('click', '#get-thumb', function(){
  var second = $('#id_second').val();
  $.ajax({
     type: 'GET',
     url: '/api/post/jq_thumb/'+video_id+'/',
     cache: 'false',
  //           contentType: 'application/json; charset=utf-8',
     dataType: 'json',
     data: {"second": second},
     success: function(response){
         d = new Date();
         $("#video-thumb").attr("src", response.url + "?"+d.getTime());
     },
     error: function(response){
         alert("Generate thumbnail error");
     }
  });
  return false;
});