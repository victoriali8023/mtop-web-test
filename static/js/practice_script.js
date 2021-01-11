

var name = document.getElementsByClassName('.watch-container');

document.getElementById("interface").src = 'static/images/practice.png';

$(document).keypress(function(e) {
	if(e.which == 13) {
    $(".watch-container").addClass("show");
    interfaceShow = true;
  }
  setInterval(function(){
    if (name.length > 15) {
        $(".watch-container").removeClass("show");
      }
  },5000);
  window.setTimeout(function(){
    window.location.href = 'firstScenario';
  }, 10000);
});