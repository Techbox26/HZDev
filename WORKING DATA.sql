-- MySQL dump 10.17  Distrib 10.3.12-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	10.3.12-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `project`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `project` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `project`;

--
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignment` (
  `assID` int(11) NOT NULL AUTO_INCREMENT,
  `assTitle` varchar(45) DEFAULT NULL,
  `taskdetails` varchar(300) DEFAULT NULL,
  `dueDate` date DEFAULT NULL,
  `assignmentFileName` varchar(45) DEFAULT NULL,
  `assignmentFilePath` varchar(80) DEFAULT NULL,
  `class_classID` int(11) NOT NULL,
  PRIMARY KEY (`assID`),
  KEY `fk_assignment_class1_idx` (`class_classID`),
  CONSTRAINT `fk_assignment_class1` FOREIGN KEY (`class_classID`) REFERENCES `class` (`classID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignment`
--

LOCK TABLES `assignment` WRITE;
/*!40000 ALTER TABLE `assignment` DISABLE KEYS */;
INSERT INTO `assignment` VALUES (12,'DOES THIS WORK tho','Test                                ','2019-02-02','Statement_20160226.pdf','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments\\Statement_20160226.pdf',1),(13,'TESTING','TESTING','2019-03-02','ZhGEqAP.jpg','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments\\ZhGEqAP.jpg',2),(14,'IT TEST','IT TEST','2019-03-02','ZhGEqAP.jpg','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments',3),(15,'TEST2','TEST2','2019-03-02','ZhGEqAP.jpg','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments',1),(16,'TEST3','TEST3','2019-03-02','ZhGEqAP.jpg','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments',2),(17,'TEST4','TEST4','2019-03-02','ZhGEqAP.jpg','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments',3),(18,'TEST5','TEST5','2019-06-06','ZhGEqAP.jpg','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments',3),(19,'TEST6','TEST6','2019-06-06','ZhGEqAP.jpg','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments',1),(20,'TEST7','TEST7','2019-06-06','ZhGEqAP.jpg','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments',2),(21,'TEST8','TEST8','2019-06-06','ZhGEqAP.jpg','/Users/Lenovo/PycharmProjects/HZdev/UPLOADS/Assignments',3);
/*!40000 ALTER TABLE `assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class` (
  `classID` int(11) NOT NULL AUTO_INCREMENT,
  `level` varchar(45) DEFAULT NULL,
  `title` varchar(45) NOT NULL,
  PRIMARY KEY (`classID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'5','Science'),(2,'5','English'),(3,'5','IT');
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classregister`
--

DROP TABLE IF EXISTS `classregister`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classregister` (
  `users_userID` int(11) NOT NULL,
  `class_classID` int(11) NOT NULL,
  KEY `fk_classregister_users_idx` (`users_userID`),
  KEY `fk_classregister_class1_idx` (`class_classID`),
  CONSTRAINT `fk_classregister_class1` FOREIGN KEY (`class_classID`) REFERENCES `class` (`classID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_classregister_users` FOREIGN KEY (`users_userID`) REFERENCES `user` (`userID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classregister`
--

LOCK TABLES `classregister` WRITE;
/*!40000 ALTER TABLE `classregister` DISABLE KEYS */;
INSERT INTO `classregister` VALUES (11,1),(11,2),(11,3),(12,1),(12,2),(12,3),(10,2),(10,3),(10,1),(8,1),(8,2),(8,3);
/*!40000 ALTER TABLE `classregister` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submission`
--

DROP TABLE IF EXISTS `submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `submission` (
  `subID` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `inputFileName` varchar(45) DEFAULT NULL,
  `inputFilePath` varchar(80) DEFAULT NULL,
  `finalmark` int(11) DEFAULT NULL,
  `teachcomment` varchar(45) DEFAULT NULL,
  `assignment_assID` int(11) NOT NULL,
  `user_userID` int(11) NOT NULL,
  PRIMARY KEY (`subID`),
  KEY `fk_submission_assignment1_idx` (`assignment_assID`),
  KEY `fk_submission_user1_idx` (`user_userID`),
  CONSTRAINT `fk_submission_assignment1` FOREIGN KEY (`assignment_assID`) REFERENCES `assignment` (`assID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_submission_user1` FOREIGN KEY (`user_userID`) REFERENCES `user` (`userID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submission`
--

LOCK TABLES `submission` WRITE;
/*!40000 ALTER TABLE `submission` DISABLE KEYS */;
INSERT INTO `submission` VALUES (4,'2019-03-03','yeet','yeet',95,'THIS IS A TEST',13,10),(5,'2019-03-03','yeet','yeet',80,'THIS IS A TEST',12,10),(10,'2019-03-03','Yeet','Yeet',65,'TEST',14,10),(12,'2019-03-03','Yeet','Yeet',NULL,NULL,18,11),(14,'2019-03-03','Yeet','Yeet',65,'TEST',14,9),(15,'2019-03-03','Yeet','Yeet',65,'TEST',14,8),(16,'2019-03-03','Yeet','Yeet',NULL,NULL,18,7),(17,'2019-03-03','Yeet','Yeet',NULL,NULL,18,6),(19,'2019-03-03','yeet','yeet',80,'THIS IS A TEST',15,10),(20,'2019-03-03','yeet','yeet',65,'THIS IS A TEST',16,10),(21,'2019-03-03','yeet','yeet',80,'THIS IS A TEST',15,8),(22,'2019-03-03','yeet','yeet',65,'THIS IS A TEST',16,8);
/*!40000 ALTER TABLE `submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(45) NOT NULL,
  `memberID` int(1) DEFAULT NULL,
  `fname` varchar(45) NOT NULL,
  `lname` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `pview` tinyint(1) NOT NULL,
  `parent_parentID` int(11) DEFAULT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'b@gmail.com',NULL,'bo','bob','bob',1,NULL),(3,'a',NULL,'a','a','a',1,NULL),(4,'example',NULL,'a','a','bam@margera.com',1,NULL),(5,'12345',NULL,'adam','adam','test@me.com',1,NULL),(6,'1234',NULL,'Adam','Lewis','adam@adam.com',1,NULL),(7,'1234',NULL,'ad','ad','ad@ad.com',1,NULL),(8,'test',NULL,'Adam','Lewis','technowhiz1@gmail.com',1,12),(9,'atest',NULL,'atest','atest','atest@atest.com',1,NULL),(10,'test',1,'TEST','STUDENT','test@test.com',1,12),(11,'testteach',2,'TEST','TEACHER','test@teacher.com',0,NULL),(12,'testparent',3,'TEST','PARENT','test@parent.com',0,NULL);
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

-- Dump completed on 2019-04-21 17:40:40
