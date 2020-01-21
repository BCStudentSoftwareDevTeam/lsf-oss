CREATE DATABASE IF NOT EXISTS `lsf`;

USE `lsf`;

CREATE TABLE IF NOT EXISTS `user` (
  `username` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `firstname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `lastname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`username`)
);


CREATE TABLE  IF NOT EXISTS `laborreleaseform` (
  `laborReleaseFormID` int(11) NOT NULL,
  `term` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `studentSupervisee_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `primarySupervisor_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `secondarySupervisor_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `departmentCode` int(11) NOT NULL,
  `department` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `jobType` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `position` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `releaseDate` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `conditionAtRelease` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `reasonForRelease` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `creator` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `createdDate` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `processed` tinyint(1) NOT NULL,
  `processedBy` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `supervisorNotes` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `laborDepartmentNotes` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`laborReleaseFormID`),
  KEY `laborreleaseform_studentSupervisee_id` (`studentSupervisee_id`),
  KEY `laborreleaseform_primarySupervisor_id` (`primarySupervisor_id`),
  KEY `laborreleaseform_secondarySupervisor_id` (`secondarySupervisor_id`),
  CONSTRAINT `laborreleaseform_ibfk_1` FOREIGN KEY (`studentSupervisee_id`) REFERENCES `user` (`username`) ON DELETE RESTRICT,
  CONSTRAINT `laborreleaseform_ibfk_2` FOREIGN KEY (`primarySupervisor_id`) REFERENCES `user` (`username`) ON DELETE RESTRICT,
  CONSTRAINT `laborreleaseform_ibfk_3` FOREIGN KEY (`secondarySupervisor_id`) REFERENCES `user` (`username`) ON DELETE RESTRICT
);


CREATE TABLE IF NOT EXISTS `laborstatusform` (
  `laborStatusFormID` int(11) NOT NULL,
  `term` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `studentSupervisee` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `primarySupervisor` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `department` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `departmentCode` int(11) NOT NULL,
  `secondarySupervisor` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `jobType` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `position` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `SummerBreakHours` int(11) DEFAULT NULL,
  `RegularTermHours` int(11) DEFAULT NULL,
  `startDate` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `endDate` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `supervisorNotes` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `creator` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `createdDate` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `laborDepartmentNotes` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `formStatus` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`laborStatusFormID`)
);


CREATE TABLE IF NOT EXISTS `term` (
  `termID` int(11) NOT NULL,
  `termName` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `termCode` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`termID`)
);


