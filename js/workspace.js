/*Wait for DOM to load before executing Javasripts*/
$(document).ready(function () {

  /*Using JQuery.floatThead library */
  $(".workspace-table").floatThead({
    position: 'absolute',
    scrollContainer: true
  });

  // remove active from all links and toggle active class to new link
  $('.nav-link').click(function() {
    $('.nav-link').removeClass('active')
    $(this).toggleClass('active');
  });

});
