CREATE DATABASE `curtain`;

USE `curtain`;

DROP TABLE IF EXISTS `curtain_details`;
CREATE TABLE IF NOT EXISTS `curtain_details` (
	`pseudo_key` int(1) AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`curtain_length` BIGINT UNSIGNED NOT NULL,
	`curtain_position` BIGINT UNSIGNED NOT NULL,
  `direction` BOOLEAN DEFAULT FALSE
);


INSERT INTO `curtain_details` (`curtain_length`, `curtain_position`, `direction`) VALUES
('0', '0', FALSE);


DROP TABLE IF EXISTS `future`;
CREATE TABLE IF NOT EXISTS `future` (
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
  `time` datetime DEFAULT CURRENT_TIMESTAMP
) CHARSET=utf8;
