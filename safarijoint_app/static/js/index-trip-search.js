$(function(){
      $('#index-search').click(function(e) {
          $.ajax({
            type: "POST",
            url: "/index-search-trip/",
            data: {
/*            'depature_date_data':  $(".datepicker[name=trip_depature_date]").val(),*/
            'trip_tag_data': $('#id_the_trip_tag option:selected').val(),
            'depature_date_data': $('#id_trip_depature_date').val(),
/*              'trip_location': $('#id_trip_location option:selected').val(),*/
            'csrfmiddlewaretoken': $("input[name = csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType : 'html'
          });
      });
});

function searchSuccess(data, textStatus, jqXHR){
  $("#index-search-results").html(data);
}
