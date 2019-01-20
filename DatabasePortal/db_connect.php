<?php
	/***************************************************
	*
	*	-Connect to db `curtain` as part of web portal
	*
	***************************************************/

	try {
		$mysql = new mysqli('localhost', 'pi', '', 'curtain') or die(mysql_error());
	}
	catch (Exception $e) {
		echo "<script>console.log('Could not get database');</script>";
	}

	/* created by: MPZinke on 01.10.19 */
?>