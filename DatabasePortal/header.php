<?php
	/***************************************************
	*
	*	-Included with every web-portal doc as redundant
	*	 import of dependencies & menu
	*
	***************************************************/

	include_once ($_SERVER['DOCUMENT_ROOT'].'/dependencies/db_connect.php');
	include_once ($_SERVER['DOCUMENT_ROOT'].'/dependencies/db_functions.php');
	
	if(filter_input(INPUT_GET, 'message')){
		echo "<script> window.onload = function() {alert('".str_replace('_', ' ', filter_input(INPUT_GET, 'message'))."');}; </script>";
	}

	{ ?>
	<html>
		<head>
			<link rel="icon" href="./Media/icon.png">
			<meta name="viewport" content="width=device-width,initial-scale=1">
			<meta name="theme-color" content="#555556"/>
			<link rel="stylesheet" type="text/css" href="./dependencies/style.css"/>
			<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
		</head>
		<header class='header'>
			<span style="font-size:30px;cursor:pointer;" onclick="openNav()" class="header">&nbsp; &#9776;</span>
		</header>
		<body class='body'>
			<div id="sideMenu">
				<a href="javascript:void(0)" class="closebtn" onclick="closeNav()" style="position:relative;left:75%;">&times;</a>
				<a href="./index.php" onclick="closeNav()">Status</a>
				<a href="./set_event.php" onclick="closeNav()">Create Event</a>
				<a href="./upcoming.php" onclick="closeNav()">Future Events</a>
			</div>
	<?php 
	} 
	/* created by: MPZinke on 01.10.19 */
?>