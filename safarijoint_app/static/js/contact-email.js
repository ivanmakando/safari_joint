$(function(){
      $('#send').click(function(e) {
        e.preventDefault();
          $.ajax({
            type: "POST",
            url: "/contactemail/",
            data: {
              'email':  $('#id_email').val(),
              'message': $('#id_message').val(),
              'csrfmiddlewaretoken': $("input[name = csrfmiddlewaretoken]").val()
            },
            success: EmailSuccess,
            dataType : 'html'
          });
      });
});

function EmailSuccess(data, textStatus, jqXHR){
  $("#no-no-no").html(data);
}
