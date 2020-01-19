<?php

include_once($_SERVER['DOCUMENT_ROOT'].'/supporting/header.php');

$fail_message = "Failed_to_set_event";

if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_curtain"]))
{
	$new_percentage_position = $_POST["open_level_display"];
	if(immediate_event($selected_curtain->curtain_id, $new_percentage_position))
		header("Location:index.php?curtain=$selected_curtain->curtain_id&message=Successfully_set_event");
	else
		header("Location:index.php?curtain=$selected_curtain->curtain_id&message=$fail_message");
}
elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["close_button"]))
{
	if(close_immediately($selected_curtain->curtain_id))
		header("Location:index.php?curtain=$selected_curtain->curtain_id&message=Close_event_set_successfully");
	else
		header("Location:index.php?curtain=$selected_curtain->curtain_id&message=$fail_message");
}
elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["open_button"]))
{
	if(open_immediately($selected_curtain->curtain_id))
		header("Location:index.php?curtain=$selected_curtain->curtain_id&message=Open_event_set_successfully");
	else
		header("Location:index.php?curtain=$selected_curtain->curtain_id&message=$fail_message");
}


if(!$selected_curtain->curtain_id) echo "<h1>SELECT A CURTAIN</h1>";
else
{
?>

<h1>Set Curtain</h1>
<form method='post'>
	<input id='open_level_display' name='open_level_display' value='<?php echo $open_percentage; ?>' 
	class='input' type='number' min='0' max='100' style='width:25%;size:24px' 
	onchange='change_slider(this);' onkeyup='change_slider(this);'/>

	<button class='button' name='set_curtain' style='display:block; margin:auto; margin-top:20px;'>Set Curtain</button>

	<table style='padding-top:20px;width:100%;' width='100%'>
		<tr width='100%'>
			<td width='20%' align='right'>
				<button name='close_button' class='button background_color' style='background-color:inherit;'>Closed</button>
			</td>
			<td width='60%' align='middle'>
				<input id='slider_input' value='<?php echo $open_percentage; ?>' type='range' 
				style='width:100%' min='0' max='100'/>
			</td>
			<td width='20%' align='left'>
				<button name='open_button' class='button' style='background-color:inherit;'>Open</button>
			</td>
		</tr>
	</table>
</form>

<!-- DISPLAY -->
<div id='curtain_display' width='60%' height='50%'>
	<div id='window_outline_main' style='height: 50%' class='window_outline'></div>
	<div id='slider_light' style='background-color:#AAAA00; margin:auto; 
									position: relative;'></div>
</div>


<script>
	// ————————————————— OPENING —————————————————
	var start_location = <?php echo $open_percentage; ?>;
	intiate_display_light();

	function intiate_display_light() {
		var window_outline = document.getElementById("window_outline_main");
		// window_outline.style.left = `${($(window).width() - $(window_outline).width()) / 2}px`;

		var slider_light = document.getElementById("slider_light");
		slider_light.style.height = `${$(window_outline).height()}px`;
		slider_light.style.width = `${start_location * $(window_outline).width() / 100}px`;
		slider_light.style["background-color"] = `#FFFF${Math.floor(start_location * 255 / 100).toString(16)}`;
	}


	function set_slider_light(width) {
		width = Math.min(width, 100);  // prevent width from going over 100
		var window_outline_width = $("#window_outline_main").width();
		var slider_light = document.getElementById("slider_light");
		slider_light.style.width = `${width * window_outline_width / 100}px`;
		slider_light.style["background-color"] = `#FFFF${Math.floor(width * 255 / 100).toString(16)}`;
	}

	function change_slider(element) {
		document.getElementById("slider_input").value = element.value;
		set_slider_light(element.value);
	}

	// Update the current slider value (each time you drag the slider handle)
	document.getElementById("slider_input").oninput = function() {
		document.getElementById("open_level_display").value = this.value;
		set_slider_light(this.value);
	}


</script>

<?php 
}


include_once($_SERVER['DOCUMENT_ROOT'].'/supporting/footer.php');
?>
