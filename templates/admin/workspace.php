<?php require('common.php'); ?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <title> My Flask App </title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Fav icon throws error in console-->
    <link rel="shortcut icon" href="#">
    <!-- Bootstrap -->
    <link rel="stylesheet" href="/static/css/bootstrap.min.css" type="text/css">
    <!-- Web App's personal bootstrap -->
    <link rel="stylesheet" href="/static/css/styles.css"  type="text/css">
    <!-- Icons from Font Awesome (the css for these files needs integrity and crossorigin)-->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.2.0/css/all.css" integrity="sha384-hWVjflwFxL6sNzntih27bfxkr27PmbbK/iSvJ+a4+0owXq79v+lsFkW54bOGbiDQ" crossorigin="anonymous">
    <!-- Sweet Sweet google fonts... -->
    <link rel="stylesheet" href="/static/css/fonts.css" type="text/css">
  </head>
  <body>
  <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow" style="display:none;">
    <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="/workspace"> School Logo</a>
    <ul class="navbar-nav px-3">
      <li class="nav-item text-nowrap">
        <a class="nav-link" href="/logout">Log out</a>
      </li>
    </ul>
  </nav>

  <div class="container-fluid">
    <div class="row">
      <nav class="col-md-2 d-none d-md-block bg-light sidebar" style="display:none;" >
        <div class="sidebar-sticky">

          <ul class="nav flex-column">
            <li class="nav-item">
              <a class="nav-link active" href="/workspace"><i class="fas fa-home"></i> Workspace </a>
            </li>
          </ul>

          <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-2 mb-1 text-muted">Control Flow</h6>

          <ul class="nav flex-column mb-2">

            <li class="nav-item">
              <a class="nav-link" href="#"><i class="fas fa-envelope"></i> Recent Requests (1-10) </a>
            </li>
            <li class="nav-item">
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

      <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4" style="display:none">

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
            <tbody id="message-list" data-counter="<?php echo (int)$db->check_changes();?>">
              <?php echo $db->get_news();?>
            </tbody>
          </table>
        </div>
      </main>
    </div>
  </div>

  <!-- Javasripts are placed at the end to load faster -->
  <!-- JQuery-->
  <script type=text/javascript src="/static/jquery-3.3.1.min.js"></script>
  <!-- Bootstrap  Core Javascrript (Includes poppers.js) -->
  <script type=text/javascript src="/static/bootstrap.min.js"></script>
  <!-- Personal Script -->
  <script type=text/javascript src="/static/script.js"></script>
  <!-- Making Table Headers stick to the top (we don't need this on every page)-->
  <script type=text/javascript src="/static/jquery.floatThead.js"></script>
  <!-- Custom Jquert, this one is general for all template so it stays here-->
  <script type=text/javascript src="/static/workspace.js"></script>

  <script>
    /* AJAX request to checker */
    function check(){
      $.ajax({
        type: 'POST',
        url: 'checker.php',
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
    //Every 20 sec check if there is new update
    setInterval(check,2500);
  </script>
  </body>
</html>
