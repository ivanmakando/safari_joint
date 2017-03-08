
$(document).click(function(){
 $("#index-search-results").css("z-index","100");
});

$(function(){
	$('#index-search').click(function(e) {
     	$("#hideIt").hide();
     	$("#result-hider").show();
    });
    $('#result-hider').click(function(e) {
     	$(".dropdown-item-hide").hide();
     	$("#result-hider").hide();
     	$("#hideIt").show();
    });
 });

$(function(){
	$('#acc-form').click(function(e) {
     	$("#hideIt").hide();
     	$("#result-hider").show();
    });
    $('#result-hider').click(function(e) {
     	$(".dropdown-item-hide").hide();
     	$("#result-hider").hide();
     	$("#hideIt").show();
    });
 });
