


var name = document.getElementsByClassName('.watch-container');


$(document).keypress(function(e) {
	if(e.which == 13) {
    console.log('added in the class');
    $(".watch-container").addClass("show");
    interfaceShow = true;
  }
  setInterval(function(){
    
    if (name.length > 15) {
        $(".watch-container").removeClass("show");
      }
  },1000);
  window.setTimeout(function(){
    window.location.href = 'firstScenario';
  }, 10000);
});