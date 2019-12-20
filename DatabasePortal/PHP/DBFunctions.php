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


// —————————————— ADD CURTAIN CHANGE ———————————————

function close_immediately()
{
	global $mysqli;

	$mysqli->query(	"INSERT INTO `future` (`desired_position`, `activated`) VALUES
						('0', FALSE);");
	return $mysqli->commit();
}


function immediate_event($position_percentage)
{
	global $mysqli;

	// get open position
	$results = $mysqli->query(	"SELECT `curtain_length` FROM `curtain_details` 
									WHERE `pseudo_key` = '1';");
	if(!$results) return false;
	$max = $results->fetch_assoc()["curtain_length"];

	// add event for now to DB
	$position = $position_percentage * $max / 100;
	$mysqli->query(	"INSERT INTO `future` (`desired_position`, `activated`) VALUES
						('$position', FALSE);");
	return $mysqli->commit();
}


function new_future_event($position_percentage, $time)
{
	if(!DateTime::createFromFormat('Y-m-d H:M:S', $time)) return false;

	// get open position
	$results = $mysqli->query(	"SELECT `curtain_length` FROM `curtain_details` 
									WHERE `pseudo_key` = '1';");
	if(!$results) return false;
	$max = $results->fetch_assoc()["curtain_length"];

	// add event for now to DB
	$position = $position_percentage * $max / 100;
	$mysqli->query(	"INSERT INTO `future` (`desired_position`, `activated`, `time`) VALUES
						('$position', FALSE, '$time');");
	return $mysqli->commit();
}


function open_immediately()
{
	global $mysqli;

	// get open position
	$results = $mysqli->query(	"SELECT `curtain_length` FROM `curtain_details` 
									WHERE `pseudo_key` = '1';");
	if(!$results) return false;
	$max = $results->fetch_assoc()["curtain_length"];

	$mysqli->query(	"INSERT INTO `future` (`desired_position`, `activated`) VALUES
						('$max', FALSE);");
	return $mysqli->commit();
}


// ————————————————— GETTERS ——————————————————


function current_state_percentage()
{
	global $mysqli;

	$results = $mysqli->query(	"SELECT `curtain_position`, `curtain_length`
									FROM `curtain_details`
									WHERE `pseudo_code` = '1';");
	if(!$results) return false;

	$results = $results->fetch_assoc();
	$length = $results["curtain_length"];
	$position = $results["curtain_position"];

	return $position / $length * 100;
}


function curtain_details()
{
	global $mysqli;

	$results = $mysqli->query(	"SELECT `curtain_position`, `curtain_length`, `direction`
									FROM `curtain_details`
									WHERE `pseudo_code` = '1';");
	if(!$results) return false;

	return $results->fetch_assoc();
}


function pending_events()
{
	global $mysqli;

	$two_minutes_ago = strtotime("-2 minutes");
	$results = $mysqli->query(	"SELECT * FROM `future`
									WHERE `activated` = FALSE
									AND `time` < '$two_minutes_ago'
									ORDER BY `time` DESC;");
	if(!$results) return true;  // error in query or $mysqli; assume worst case of pending events
	return $results->num_rows;
}


function upcoming_events()
{
	global $mysqli;

	$results = $mysqli->query(	"SELECT * FROM `future`
									WHERE `activated` = FALSE
									ORDER BY `time` DESC;");
	if(!$results) return false;

	$events = array();
	while($row = $results->fetch_assoc()) $events[] = $row;

	return $row;
}


// ————————————————— SETTERS ———————————————————

function delete_event($key)
{
	global $mysqli;

	$mysqli->query(	"UPDATE `future` SET `activated` = TRUE
									WHERE `event_key` = '$key';");
	return $mysqli->commit();
}


function edit_event_position($event_key, $position)
{
	global $mysqli;

	$mysqli->query(	"UPDATE `future` SET `` = ''
						WHERE `event_key` = '$event_key';");
	return $mysqli->commit();
}


function edit_event_time($event_key, $time)
{
	global $mysqli;

	$mysqli->query(	"UPDATE `future` SET `` = ''
						WHERE `event_key` = '$event_key';");
	return $mysqli->commit();
}


// ———— DB SETTERS ————

function set_DB_direction($direction)
{
	global $mysqli;

	$mysqli->query(	"UPDATE `curtain_details` SET `direction` = '$direction'
						WHERE `pseudo_key` = '1';");
	return $mysqli->commit();
}


function set_DB_length($length)
{
	global $mysqli;

	$mysqli->query(	"UPDATE `curtain_details` SET `curtain_length` = '$length'
						WHERE `pseudo_key` = '1';");
	return $mysqli->commit();
}


function set_DB_position($position)
{
	global $mysqli;

	$mysqli->query(	"UPDATE `curtain_details` SET `curtain_position` = '$position'
						WHERE `pseudo_key` = '1';");
	return $mysqli->commit();
}


?>