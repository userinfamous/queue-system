/*Wait for DOM to load before executing Javasripts*/
$(document).ready(function () {

  /* Set message flashes*/
  setTimeout(function() {
      $('.flashes').slideUp('fast');
  }, 2500); /* in milliseconds (2.5 seconds) */


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


  //Real time pusher API, using websocket to connect to a channel
  var pusher = new Pusher('eefbd3472aabb2b3fc60', {
    cluster: 'ap1',
    encrypted: true
  });

  //Subscribing to channel after post request from "request_info"
  var channel = pusher.subscribe('queue-channel');
  channel.bind('queue-event', function(data) {
    const table = `
        <tr>
          <td>${data.Number}</td>
          <td>${data.User_type}</td>
          <td>${data.Parent_name}</td>
          <td>${data.Student_name}</td>
          <td>${data.Student_id}</td>
          <td>${data.Request_type}</td>
          <td>${data.Status}</td>
        </tr>
        `;
    let list = document.querySelector("#queue-data")
    list.innerHTML += table;
  });
});
