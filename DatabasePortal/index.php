<?php 
	/***************************************************
	*
	*	-Main page of local portal to curtains
	*	-Display current state of curtain
	*
	***************************************************/

	include_once ($_SERVER['DOCUMENT_ROOT'].'/dependencies/header.php');
	{ ?>
		<title> Curtain State </title>

		<div id='state_title' class='title'>
			<h1>Current State</h1>
		</div>
		<div id='state_state'>
		<?php
			$status = get_status();
			if(is_null($status)) echo "Unknown";
			else {
				$state = get_state_string($status);
				if($state == "Close") $state .= "d";
				echo $state;
			}
		?>
		</div>
		<div id='state_refresh'>
			<a href='./'>
				<button class='button'>Refresh</button>
			</a>
		</div>

	<?php 
	include_once ($_SERVER['DOCUMENT_ROOT'].'/dependencies/footer.php');
	}
	/* created by: MPZinke on 01.10.19 */
?>