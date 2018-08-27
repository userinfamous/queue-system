/*Wait for DOM to load before executing Javasripts*/
$(document).ready(function () {
  $('li.nav-item , h6.sidebar-heading').css('opacity', '0');
  $('nav.navbar').fadeIn("fast");
  $('main').slideDown("fast");
  $('nav.sidebar').animate({width:'toggle'},"normal"
  ,function() {
    $('li.nav-item').animate({opacity:1},"normal");
    $('h6.sidebar-heading').animate({opacity:1},"normal");
  });


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
