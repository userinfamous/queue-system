$(document).ready(function () {
  /* Set message flashes*/
  $('.flashes').slideDown(300);
  setTimeout(function() {
  $('.flashes').slideUp(300);
  }, 1500); /* in milliseconds (2.5 seconds) */

  /*End User Pages*/
  $('h3.fadeinFirst').fadeIn("slow", function() {
    $('div.fadeinSecond').fadeIn("slow");
  });

});
