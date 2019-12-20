<?php

/***********************************************************************************************************
*
*	created by: MPZinke
*	on ..
*
*	DESCRIPTION: TEMPLATE
*	BUGS:
*	FUTURE:
*
***********************************************************************************************************/


include_once("/database/DBConnect.php");
include_once("/database/DBFunctions.php");


if(pending_events()) echo_error("There is a pending event preventing proper operation of curtain");


if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["get_state"]))
{
	$state = current_state_percentage();
	if($state === false) echo_error("Could not connect to DB");
	echo json_encode(array("state" => $state));
}

// ————————————————— EVENTS ———————————————————
// ————————————————————————————————————————

// ———— GET EVENTS ————

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["unactivated_events"]))
{

}

// ———— EDIT EVENTS ————

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["delete_event"]))
{

}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["edit_event_time"]))
{

}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["edit_event_position"]))
{

}

// ———— SET EVENTS ————

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["future_event"]))
{
	if(!in_array("time", $_POST) || !in_array("position", $_POST))
		echo_error("Value missing from AJAX request");

	$time = $_POST["time"];
	$position = $_POST["position"];
	new_future_event($position, $time);
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["close"]))
{
	if(close_immediately())
		echo_success();
	echo_error("Could not set curtain to closed");
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["open"]))
{
	if(open_immediately())
		echo_success();
	echo_error("Could not set curtain to open");
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["immediate_event"]))
{
	if(!in_array("position", $_POST)) echo_error("Value missing from AJAX request");

	$position = $_POST["position"];
	if(immediate_event($position))
		echo_success();
	echo_error("Could not set curtain event");
}


// ———————————————— DB DETAILS ——————————————————
// ————————————————————————————————————————

// ———— GET DB DETAILS ————

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["get_DB_details"]))
{

}

// ———— SET DB DETAILS ————

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_direction"]))
{
	//TODO
	set_DB_direction();
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_length"]))
{
	//TODO
	set_DB_length();
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_position"]))
{
	//TODO
	set_DB_position();
}


else
{
	echo_error("Unknown request");
}



function echo_error($error_message)
{
	echo json_encode(array("error" => $error_message));
	exit();
}

function echo_success($message=null)
{
	if($message) echo json_encode(array("message" => $message, "success" => true));
	else echo json_encode(array("success" => true));
	exit();
}


?>