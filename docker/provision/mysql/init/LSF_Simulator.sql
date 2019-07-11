-- MySQL dump 10.13  Distrib 8.0.16, for macos10.14 (x86_64)
--
-- Host: 127.0.0.1    Database: lsf
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `laborreleaseform`
--

DROP TABLE IF EXISTS `laborreleaseform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `laborreleaseform` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laborreleaseform`
--

LOCK TABLES `laborreleaseform` WRITE;
/*!40000 ALTER TABLE `laborreleaseform` DISABLE KEYS */;
/*!40000 ALTER TABLE `laborreleaseform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `laborstatusform`
--

DROP TABLE IF EXISTS `laborstatusform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `laborstatusform` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laborstatusform`
--

LOCK TABLES `laborstatusform` WRITE;
/*!40000 ALTER TABLE `laborstatusform` DISABLE KEYS */;
/*!40000 ALTER TABLE `laborstatusform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `migratehistory`
--

DROP TABLE IF EXISTS `migratehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `migratehistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `migrated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `migratehistory`
--

LOCK TABLES `migratehistory` WRITE;
/*!40000 ALTER TABLE `migratehistory` DISABLE KEYS */;
INSERT INTO `migratehistory` VALUES (1,'0001_migration_201907032323','2019-07-04 03:23:23'),(2,'0002_migration_201907032325','2019-07-04 03:25:40'),(3,'0003_migration_201907040004','2019-07-04 04:05:18'),(4,'0004_migration_201907040007','2019-07-04 04:07:58'),(5,'0005_migration_201907042110','2019-07-05 01:13:33'),(6,'0006_migration_201907080925','2019-07-08 13:25:38'),(7,'0007_migration_201907080926','2019-07-08 13:26:57'),(8,'0008_migration_201907090015','2019-07-09 04:15:41'),(9,'0009_migration_201907090015','2019-07-09 04:15:41');
/*!40000 ALTER TABLE `migratehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `term`
--

DROP TABLE IF EXISTS `term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `term` (
  `termID` int(11) NOT NULL,
  `termName` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `termCode` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`termID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `term`
--

LOCK TABLES `term` WRITE;
/*!40000 ALTER TABLE `term` DISABLE KEYS */;
/*!40000 ALTER TABLE `term` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `username` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `firstname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `lastname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-11  8:50:59
