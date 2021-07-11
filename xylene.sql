-- MySQL dump 10.13  Distrib 8.0.23, for macos10.15 (x86_64)
--
-- Host: localhost    Database: xylene
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `documents`
--

DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents` (
  `pk` int NOT NULL AUTO_INCREMENT,
  `username_created` varchar(64) DEFAULT NULL,
  `username_updated` varchar(64) DEFAULT NULL,
  `updated` varchar(64) DEFAULT NULL,
  `docnum` varchar(10) DEFAULT NULL,
  `field_name` varchar(255) DEFAULT NULL,
  `data` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pk`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
INSERT INTO `documents` VALUES (1,'david','david','2021-07-05 11:42:55','100001','trustee_sale_date','2021-04-06'),(2,'david','david','2021-07-05 11:43:06','100001','county','Harris'),(3,'david','david','2021-07-05 11:43:17','100001','foreclosure_type','hoa/condo'),(4,'david','david','2021-07-05 11:43:22','100001','legal_block','1'),(5,'david','david','2021-07-05 11:43:47','100001','legal_lot','2'),(6,'david','david','2021-07-05 11:44:14','100001','legal_subdivision','bbb'),(7,'david','jeremy','2021-07-05 11:56:58','100001','deed_of_trust_year','2018'),(8,'david','jeremy','2021-07-05 11:59:13','100001','original_loan_amount','75'),(9,'david','david','2021-07-05 12:01:00','100001','borrower_name','richard nixon'),(10,'david','david','2021-07-05 12:01:13','100001','owner_name','pat nixon'),(11,'david','david','2021-07-05 12:02:03','100001','greeting','pat'),(12,'david','david','2021-07-05 12:02:25','100001','property_address','813 e mitchell ave\r\nwaco tx 76704'),(13,'david','david','2021-07-05 12:03:16','100001','market_value','12'),(14,'david','david','2021-07-05 12:03:49','100001','owner_mailing1','813 e mitchell ave\r\nwaco tx 76704'),(15,'david','david','2021-07-05 12:04:09','100001','owner_mailing2','unk'),(16,'david','david','2021-07-05 12:04:17','100001','status','complete'),(17,'david','david','2021-07-05 11:43:12','100002','trustee_sale_date','2021-08-03'),(18,'david','david','2021-07-05 11:43:27','100002','county','Travis'),(19,'david','david','2021-07-05 11:43:41','100002','foreclosure_type','reverse mortgage'),(20,'david','david','2021-07-05 11:43:51','100002','legal_block','3'),(21,'david','david','2021-07-05 11:43:57','100002','legal_lot','4'),(22,'david','david','2021-07-05 11:44:02','100002','legal_subdivision','aaa'),(23,'david','david','2021-07-05 11:44:08','100002','deed_of_trust_year','2009'),(24,'david','david','2021-07-05 12:00:12','100002','original_loan_amount','12'),(25,'david','david','2021-07-05 12:01:52','100002','borrower_name','harry truman'),(26,'david','david','2021-07-05 12:01:57','100002','owner_name','harry truman'),(27,'david','david','2021-07-05 12:02:11','100002','greeting','mr truman'),(28,'david','david','2021-07-05 12:02:42','100002','property_address','209 alamosa drive\r\nhewitt tx 76643'),(29,'david','david','2021-07-05 12:03:03','100002','market_value','8'),(30,'david','david','2021-07-05 12:03:08','100002','owner_mailing1','209 alamosa drive\r\nhewitt tx 76643'),(31,'david','david','2021-07-05 12:03:39','100002','owner_mailing2','unk'),(32,'david','david','2021-07-05 12:03:53','100002','status','complete'),(33,'jeremy','jeremy','2021-07-05 11:58:08','100003','trustee_sale_date','2021-06-01'),(34,'jeremy','jeremy','2021-07-05 11:58:12','100003','county','Williamson'),(35,'jeremy','jeremy','2021-07-05 11:58:17','100003','foreclosure_type','bank mortgage'),(36,'jeremy','jeremy','2021-07-05 11:58:42','100003','legal_block','7'),(37,'jeremy','jeremy','2021-07-05 11:59:06','100003','legal_lot','8'),(38,'jeremy','jeremy','2021-07-05 11:59:21','100003','legal_subdivision','ccc'),(39,'jeremy','david','2021-07-05 12:00:17','100003','deed_of_trust_year','2007'),(40,'jeremy','david','2021-07-05 12:00:26','100003','original_loan_amount','99'),(41,'jeremy','david','2021-07-05 12:00:50','100003','borrower_name','ronald reagan'),(42,'jeremy','david','2021-07-05 12:01:06','100003','owner_name','ronald reagan'),(43,'jeremy','david','2021-07-05 12:01:22','100003','greeting','ronald'),(44,'jeremy','david','2021-07-05 12:01:35','100003','property_address','1801 n 13th st\r\nwaco tx 76707'),(45,'jeremy','david','2021-07-05 12:01:42','100003','market_value','66'),(46,'jeremy','david','2021-07-05 12:03:33','100003','owner_mailing1','1825 n 13th st\r\nwaco tx 76707'),(47,'jeremy','david','2021-07-05 12:04:03','100003','owner_mailing2','unk'),(48,'jeremy','david','2021-07-05 12:04:22','100003','status','complete'),(49,'jeremy','jeremy','2021-07-05 17:23:50','100004','trustee_sale_date','2021-09-07'),(50,'jeremy','jeremy','2021-07-05 17:23:43','100004','county','blank'),(51,'jeremy','jeremy','2021-07-05 17:23:43','100004','foreclosure_type','blank'),(52,'jeremy','jeremy','2021-07-05 17:23:43','100004','legal_block','blank'),(53,'jeremy','jeremy','2021-07-05 17:23:43','100004','legal_lot','blank'),(54,'jeremy','jeremy','2021-07-05 17:23:43','100004','legal_subdivision','blank'),(55,'jeremy','jeremy','2021-07-05 17:23:43','100004','deed_of_trust_year','blank'),(56,'jeremy','jeremy','2021-07-05 17:23:43','100004','original_loan_amount','blank'),(57,'jeremy','jeremy','2021-07-05 17:23:43','100004','borrower_name','blank'),(58,'jeremy','jeremy','2021-07-05 17:23:43','100004','owner_name','blank'),(59,'jeremy','jeremy','2021-07-05 17:23:43','100004','greeting','blank'),(60,'jeremy','jeremy','2021-07-05 17:23:43','100004','property_address','blank'),(61,'jeremy','jeremy','2021-07-05 17:23:43','100004','market_value','blank'),(62,'jeremy','jeremy','2021-07-05 17:23:43','100004','owner_mailing1','blank'),(63,'jeremy','jeremy','2021-07-05 17:23:43','100004','owner_mailing2','blank'),(64,'jeremy','jeremy','2021-07-05 17:23:43','100004','status','incomplete'),(65,'jeremy','jeremy','2021-07-08 07:55:04','100001','response','rrreee'),(66,'jeremy','jeremy','2021-07-08 07:58:12','100001','response','rrreee'),(67,'jeremy','jeremy','2021-07-08 08:17:35','100001','response','ggg'),(68,'jeremy','jeremy','2021-07-08 08:17:40','100001','response','ggg'),(69,'jeremy','jeremy','2021-07-08 08:18:12','100001','response','ggg'),(70,'jeremy','jeremy','2021-07-08 18:53:50','100002','response','yyy'),(71,'jeremy','jeremy','2021-07-08 18:53:53','100002','response','yyy'),(72,'jeremy','jeremy','2021-07-08 18:55:27','100002','response','yyy'),(73,'jeremy','jeremy','2021-07-08 18:56:25','100002','response','yyy'),(74,'jeremy','jeremy','2021-07-08 18:58:03','100002','response','yyy'),(75,'jeremy','jeremy','2021-07-08 18:58:36','100002','response','yyy'),(78,'jeremy','jeremy','2021-07-09 06:17:48','100002','return_mail','owner_mailing1'),(79,'david','david','2021-07-09 07:18:59','100002','return_mail','owner_mailing1'),(80,'david','david','2021-07-09 07:19:22','100002','response','who'),(81,'david','david','2021-07-09 07:19:27','100002','response','who'),(82,'david','david','2021-07-09 07:21:39','100003','return_mail','owner_mailing1'),(83,'david','david','2021-07-09 07:25:25','100001','response','blahhhhhhhhhhhhhhhhh'),(84,'david','david','2021-07-09 07:25:35','100001','response','blahhhhhhhhhhhhhhhhh'),(85,'david','david','2021-07-09 07:32:54','100002','return_mail','owner_mailing1'),(86,'david','david','2021-07-09 07:46:31','100002','response','what'),(87,'david','david','2021-07-09 07:47:09','100001','response','four score');
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-11  7:15:01
