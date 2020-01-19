<?php
	/***************************************************
	*
	*	-Function to be use for/with db `curtain` as
	*	 part of local portal
	*
	***************************************************/

	function get_status() {
		global $mysql;

		if($status = $mysql->query("SELECT `state`
								 FROM `state`;"
		)) {
			return $status->fetch_object()->state;
		}
		return false;
	}

	function get_state_string($state_char) {
		if($state_char == 'O') return "Open";
		else if($state_char == 'C') return "Close";
		else if($state_char == 'W') return "In Operation";
		else return "Unknown";
	}

	function set_future_event($event_action, $event_time) {
		global $mysql;

		if($mysql->query("INSERT INTO `future` (`event_action`, `event_time`) VALUES ('$event_action', '$event_time');")) {
			return true;
		}
		return false;
	}

	function get_future_events() {
		global $mysql;

		if($result = $mysql->query("SELECT * FROM `future` WHERE `event_time` >= NOW() ORDER BY `event_time`;")) {
			$events = array();
			while($row = $result->fetch_assoc()) {
				$events[] = $row;
			}
			return $events;
		}
		return null;
	}

	function get_day($time) {
		$time = strtotime($time);
		if(date('Y-m-d', $time) == date('Y-m-d')) return "Today";
		else if(date('Y-m-d', $time) == date('Y-m-d', strtotime("+1 day"))) return "Tomorrow";
		return date('D', $time);
	}

	function remove_events($value_string) {
		global $mysql;

		$failures = 0;
		$values = explode('|', $value_string, substr_count($value_string, '|')+1);
		foreach($values as $val) {
			if(!$mysql->query("DELETE FROM `future` WHERE `event_time` = '$val';")) {
				$failures++;
			}
		}
		return $failure;
	}
	/* created by: MPZinke on 01.10.19 */
?>