CREATE DATABASE `curtain`;

USE `curtain`;

DROP TABLE IF EXISTS `curtain_details`;
CREATE TABLE IF NOT EXISTS `curtain_details` (
	`pseudo_key` int(1) AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`curtain_length` BIGINT UNSIGNED NOT NULL,
	`curtain_position` BIGINT UNSIGNED NOT NULL,
	`direction` BOOLEAN DEFAULT FALSE
);


DROP TABLE IF EXISTS `options`;
CREATE TABLE IF NOT EXISTS `options` (
	`pseudo_key` int(1) AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`adafruit_feed` BOOLEAN DEFAULT FALSE,
	`event_prediction` BOOLEAN DEFAULT FALSE,
	`sunrise_open` BOOLEAN DEFAULT FALSE,
	`sunset_close` BOOLEAN DEFAULT FALSE
);


INSERT INTO `curtain_details` (`curtain_length`, `curtain_position`, `direction`) VALUES
('0', '0', FALSE);


DROP TABLE IF EXISTS `events`;
CREATE TABLE IF NOT EXISTS `events` (
	`event_key` int(11) AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`desired_position` BIGINT UNSIGNED NOT NULL,
	`activated` BOOLEAN DEFAULT TRUE,
	`time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARSET=utf8;


DROP TABLE IF EXISTS `error_log`;
CREATE TABLE IF NOT EXISTS `error_log` (
	`error_log_key` int(11) AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`curtain_position` BIGINT UNSIGNED NOT NULL,
	`desired_position` BIGINT UNSIGNED NOT NULL,
	`error` text DEFAULT NULL,
	`path` text DEFAULT NULL,
	`time` datetime DEFAULT CURRENT_TIMESTAMP
) CHARSET=utf8;
