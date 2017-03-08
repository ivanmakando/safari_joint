$(document).click(function(){
 $(".dropdown-item-hide").hide('slow');
});

$(".dropdown-item-hide").click(function(e){
  e.stopPropagation();
});