$(function(){
      $('#search-bookings').click(function(e) {
        e.preventDefault();
          $.ajax({
            type: "POST",
            url: $(this).data('url'),
            data: {
              'serial_number':  $('#id_serial_number').val(),
              'name': $('#id_name').val(),
              'booking_date': $('#id_booking_date').val(),
              'csrfmiddlewaretoken': $("input[name = csrfmiddlewaretoken]").val()
            },
            success: searchTripBookings,
            dataType : 'html'
          });
      });
});

function searchTripBookings(data, textStatus, jqXHR){
  $("#booking-search-results").html(data);
}
