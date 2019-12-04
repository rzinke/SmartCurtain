<?php 
	/***************************************************
	*
	*	-Main page of local portal to curtains
	*	-Display current state of curtain
	*
	***************************************************/
	include_once ($_SERVER['DOCUMENT_ROOT'].'/dependencies/header.php');

	$status = get_status();
	if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['toggle_curtain'])) {
		if($status == "O" || $status == "C")  {
			echo '<script>';
			if(set_future_event($status == 'O' ? 'C' : 'O', date('Y-m-d H:i:s'))) 
				echo 'alert("Successfully created event");';
			else echo 'alert("Could not set event");';
			echo 'window.location.href = "./";'.
			'</script>';
		}
	}

	$opposites = array('O' => "Close", 'C' => "Open", 'W' => "In Operation");

	?>
		<title> Curtain State </title>

		<div id='state_title' class='title'>
			<h1>Current State</h1>
		</div>
		<div id='state_state'>
		<?php
			if(is_null($status)) echo "Unknown";
			else {
				$state = get_state_string($status);
				if($state == "Close") $state .= "d";
				echo $state;
			}
		?>
		</div>
		<div id='toggle_state'>
			<form method='POST'>
				<button name='toggle_curtain' type='submit' class='button'> <?php echo $opposites[get_status()]; ?> </button>
			</form>
		</div>

	<?php 
	include_once ($_SERVER['DOCUMENT_ROOT'].'/dependencies/footer.php');
	/* created by: MPZinke on 01.10.19
	    edited to contain immediate opening of curtain */
?>
<script>
	var state = document.getElementById("state_state").textContent.trim();
	if(state == "In Operation") setTimeout(function() {window.location.href = "./";}, 2000);
</script>