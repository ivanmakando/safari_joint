$(function(){
      $('#search').keyup(function() {
          $.ajax({
            type: "POST",
            url: "/search/",
            data: {
              'search_text': $('#search').val(),
              'csrfmiddlewaretoken': $("input[name = csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType : 'html'
          });
      });
});

function searchSuccess(data, textStatus, jqHXR){
  $("#search-results").html(data);
}
