<?php

class Event
{
	public $event_id;
	public $curtain_id;
	public $event_position;
	public $event_activated;
	public $event_time;

	function __construct($event_id)
	{
		global $mysqli;

		$results = $mysqli->query(	"SELECT * FROM `events` 
										WHERE `event_id` = $event_id");
		if(!$results) return $this->null_all_values();

		$results = $results->fetch_assoc();
		$this->event_id = $results["event_id;"];
		$this->curtain_id = $results["curtain_id;"];
		$this->event_position = $results["event_position;"];
		$this->event_activated = $results["event_activated;"];
		$this->event_time = $results["event_time;"];
	}


	private function null_all_values()
	{
		foreach($this as $key => $value) unset($this->$key);
	}
}


?>