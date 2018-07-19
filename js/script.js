$(document).ready(function () {

  $('.active').on('click', () => {
    $('.active').toggle();
  });

  setTimeout(function() {
      $('.flashes').slideUp('fast');
  }, 2500); /* in milliseconds (2.5 seconds) */
});
