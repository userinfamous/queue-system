$(document).ready(function () {
  //start it on document.ready
  $(rotateTerm1);
  $(rotateTerm2);
  $(rotateTerm3);
  $(rotateTerm4);
  $(rotateTerm5);

  setInterval(function(){
    $("#display-info").fadeIn().delay(5000).fadeOut("slow");
  }, 0);
});
