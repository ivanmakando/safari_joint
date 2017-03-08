$(function(){
      $('#feed-button').click(function(e) {
        e.preventDefault();
          $.ajax({
            type: "POST",
            url: $(this).data('url'),
            data: {
              'feed_body':  $('#id_feed_body').val(),
              'posted_by': $('#id_posted_by').val(),
              'visit_date': $('#id_visit_date').val(),
              'csrfmiddlewaretoken': $("input[name = csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,

            /*complete : completedFeed, */

            dataType : 'html'
          });
      });
});

function searchSuccess(data, textStatus, jqXHR){
  $(".alert").fadeOut();
  $(".alert-success").html('Thank You!');
  $(".alert-success").fadeIn(600);
}
