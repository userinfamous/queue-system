<?php require('common.php');
if ($_POST['Confirm']) {
	$result = $db->register_changes();
}?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Add news - Demo for Ajax Autorefresh</title>
</head>
<body>
	<h1>This is a demo for post <a href="http://blog.codebusters.pl/en/entry/ajax-auto-refresh-volume-ii">Ajax Auto Refresh - Volume II</a></h1>
	<p>Open <a href="index.php">list of messages</a> in new window, add new message with this form and look at that list. Don't refresh it manually. It should refresh automatically after 20 seconds.<p>
	<?php if(isset($result)){
		if($result==TRUE){
			echo '<p>Success</p>';
		}else{
			echo '<p>Error</p>';
		}
	}else{?>
		<form method="post" action="#">
			<input type="text" name="title" size="50" />
			<input type="submit" value="Add message" />
		</form>
	<?php }?>
</body>
</html>
