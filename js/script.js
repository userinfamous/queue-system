$(document).ready(function () {

  $('.active').on('click', () => {
    $('.active').toggle();
  });

  setTimeout(function() {
      $('.flashes').delay(50).slideUp(250);
  }, 300);
});
