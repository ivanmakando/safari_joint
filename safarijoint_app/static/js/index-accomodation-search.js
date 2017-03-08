$(function(){
      $('#acc-form').click(function(e) {
        e.preventDefault();
          $.ajax({
            type: "POST",
            url: "/index-search-accomodation/",
            data: {
              'arrival_date_data':  $('#id_arrival_date').val(),
              'room_type_data': $('#id_room_type option:selected').val(),
                'destination_data': $('#id_destination option:selected').val(),
    /*        'include_airport_transport_data': htmlEncode($('#div_id_include_airport_transport').attr('checked'))*/
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
