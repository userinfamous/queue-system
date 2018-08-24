<?php require('common.php'); ?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Demo for Ajax Auto Refresh</title>
	<script src="jquery-1.10.2.min.js"></script>
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
</head>
<body>
	<h1>This is a demo for post <a href="http://blog.codebusters.pl/en/entry/ajax-auto-refresh-volume-ii">Ajax Auto Refresh - Volume II</a></h1>
	<?php /* Our message container. data-counter should contain initial value of couner from database */ ?>
	<div id="message-list" data-counter="<?php echo (int)$db->check_changes();?>">
		<?php echo $db->get_news();?>
	</div>
	<p><a href="add.php">Add new message</a></p>
</body>
</html>
