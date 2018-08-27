$(document).ready(function () {
  /* Set message flashes*/
  $('.flashes').slideDown(300);
  setTimeout(function() {
  $('.flashes').slideUp(300);
  }, 1500); /* in milliseconds (2.5 seconds) */

  /*End User Pages*/
  $('div.fadein').fadeIn("normal");

});
