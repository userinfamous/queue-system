<?php
define('__ROOT__', dirname(dirname(__FILE__)));
require(__ROOT__.'/common.php');
?>
{% extends 'layout.html' %}

{% block body %}
  {% from "includes/_form_helpers.html" import render_field %}

  <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
    <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="/workspace"> School Logo</a>
    <ul class="navbar-nav px-3">
      <li class="nav-item text-nowrap">
        <a class="nav-link" href="/logout">Log out</a>
      </li>
    </ul>
  </nav>


  <div class="container-fluid">
    <div class="row">
      <nav class="col-md-2 d-none d-md-block bg-light sidebar">
        <div class="sidebar-sticky">

          <ul class="nav flex-column">
            <li class="nav-item">
              <a class="nav-link active" href="/workspace"><i class="fas fa-home"></i> Workspace </a>
            </li>
          </ul>

          <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
            <span>Control Flow</span>
          </h6>

          <ul class="nav flex-column mb-2">

            <li class="nav-item">
              <a class="nav-link" href="#"><i class="fas fa-envelope"></i> Recent Requests (1-10) </a>
            </li>

            <li class="av-item">
              <a class="nav-link" href="#"><i class="fas fa-archive"></i> Archive </a>
            </li>

            <li class="nav-item">
              <a class="nav-link" href="#"><i class="fas fa-undo"></i> Undo </a>
            </li>

            <li class="nav-item">
              <a class="nav-link" href="#"><i class="fas fa-expand-arrows-alt"></i> Reassign </a>
            </li>

          </ul>
        </div>
      </nav>

      <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">

        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
          <h1> {{session.department}} Queue</h1>
        </div>

        <div class="table-responsive queue-container">
          <table  class=" table table-striped table-sm workspace-table">
            <thead>
              <tr>
                <th>User Type </th>
                <th>Contact </th>
                <th>Parent Name</th>
                <th>Student Name</th>
                <th>ID</th>
                <th>Request Type</th>
                <th>Status</th>
                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <!-- Queue Container -->
              <div id="message-list" data-counter="<?php echo (int) $db->check_changes();?>">
                <?php echo $db->get_news();?>
              </div>
              {% for queue in queues %}
              <tr>
                <td>
                <!-- If the queue is on top -->
                {% if queue == queues[0] %}
                  {% if queue.Status == 'Waiting' %}
                  <form action="{{url_for('entry_call', number=queue.Number)}}" method="POST">
                    <input type="hidden" name="method" value="CALL">
                    <input id="call-button" type="submit" value="Call Number" class="btn btn-warning">
                  </form>
                  {% else %} <!-- If status is in progress or admin pressed Call Number, load the reassign table -->
                    {{queue.Status}}
                </td>
                <!-- This might confuse you, but we want to load a whole table when as the above, we just want the data -->
                <td align="right">
                  <form action="" method="POST">
                    {{render_field(form.en_Assign, class="submit-button")}}
                    <input id="reassign-button" type="submit" value="Reassign" class="btn btn-info">
                  </form>
                </td>
                  {% endif %}
                <td align="left">
                  {% if queue.Status == 'In Progress' %}
                  <form action="{{url_for('entry_complete', number=queue.Number)}}" method="POST">
                    <input type="hidden" name="method" value="COMPLETE">
                    <input id="complete-button" type="submit" value="Complete" class="btn btn-success">
                  </form>
                </td>
                  {% endif %}
                {% else %}
                <td></td>
                <td></td>
                <td></td>
                {% endif %}
              {% endfor %}
              </tr>
            </tbody>
          </table>
          <!-- Display No Queue Message -->
          {% if no_queue %}
            <h3 class="text-center" id="queue-message">{{no_queue}}</h3>
          {% endif %}
        </div>
      </main>
    </div>
  </div>

{% endblock %}

{% block custom_scripts %}
<!-- Making Table Headers stick to the top (we don't need this on every page)-->
<script src="https://cdnjs.cloudflare.com/ajax/libs/floatthead/2.1.2/jquery.floatThead.js"></script>
<!-- Custom Jquert, this one is general for all template so it stays here-->
<script src="http://localhost/js/workspace.js"></script>

<script>
  /* AJAX request to checker */
  function check(){
    $.ajax({
      type: 'POST',
      url: 'checker',
      dataType: 'json',
      data: {
        counter:$('#message-list').data('counter')
      }
    }).done(function( response ) {
      /* update counter */
      $('#message-list').data('counter',response.current);
      /* check if with response we got a new update */
      if(response.update==true){
        $('#message-list').html(response.news);
      }
    });
  }
  //Every 0.5 sec check if there is new update
  setInterval(check,2500);
</script>
{% endblock %}
