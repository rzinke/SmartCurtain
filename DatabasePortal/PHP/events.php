<?php

include_once($_SERVER['DOCUMENT_ROOT'].'/supporting/header.php');
?>

<h1>Events</h1>
<button onclick='collapse_expand_div(this, "#create_event_div", "Create Event");' class='button'>Create Event</button>
<div id='create_event_div' hidden>
	<form>
		<input type='date' value='<?php echo date();?>' onchange='update_prior_position(this);' class='input'>

	</form>

	<!-- DISPLAY -->

	<div style='padding-bottom: 3px;'>
		<div class='window_outline' style='height: 9px; background-color: #333366'></div>
		<div id='current_light' style='background-color:#AAAA00; margin:auto; position: relative;
										height: 5px;'></div>
	</div>
	<div id='curtain_display' width='60%' height='50%'>
		<div id='window_outline_main' style='height: 50%' class='window_outline'></div>
		<div id='slider_light' style='background-color:#AAAA00; margin:auto; 
										position: relative;'></div>
	</div>
</div>

<?php
include_once($_SERVER['DOCUMENT_ROOT'].'/supporting/footer.php');
?>

<script>
	function update_prior_position(element)
	{
		// ajax stuff to get position leading up to time
	}

</script>