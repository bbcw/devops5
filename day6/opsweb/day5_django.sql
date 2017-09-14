-- MySQL dump 10.13  Distrib 5.6.37, for Linux (x86_64)
--
-- Host: localhost    Database: django
-- ------------------------------------------------------
-- Server version	5.6.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'devops'),(2,'op'),(3,'产品组'),(5,'运维组');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (15,5,22);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add person',7,'add_person'),(20,'Can change person',7,'change_person'),(21,'Can delete person',7,'delete_person'),(22,'Can add idc',8,'add_idc'),(23,'Can change idc',8,'change_idc'),(24,'Can delete idc',8,'delete_idc'),(25,'访问idc列表权限',8,'view_idc');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$36000$Tj5O2Wi0mmyi$8bWyU8LxnUVamlrkhoiWc/QmmukRn5A/VtrvwI8pMCk=','2017-09-03 09:49:42.597075',0,'rock','','','rock@51reboot.com',0,1,'2017-08-06 08:12:54.436036'),(4,'pbkdf2_sha256$36000$WcZP5RyDFPfQ$R24NDKmcxx4o4lZOyjpywdFIJhoE9POPNC/Yc0bd4pU=','2017-08-20 05:59:24.503408',0,'rock-1','','','rock-1@51reboot.com',0,1,'2017-08-13 03:34:33.034834'),(5,'pbkdf2_sha256$36000$P1iA4FmP9CFu$00gsJRzL75LqI1JA/RcCgXjnvu+E75nnc1V00g/aaUk=',NULL,0,'rock-2','','','rock-2@51reboot.com',0,0,'2017-08-13 03:34:33.186878'),(6,'pbkdf2_sha256$36000$G4gu5mIoupeJ$W8dekcwELkhPdgZQRFlTLHBuk7q35ANrgJe/N+sXtr4=',NULL,0,'rock-3','','','rock-3@51reboot.com',0,1,'2017-08-13 03:34:33.309858'),(7,'pbkdf2_sha256$36000$7vgrr2iLpDeo$F6/BMrsWi9auFVQFgk7H1vKGGWK0I8/EbYi9MO73KGc=','2017-08-20 10:44:20.375094',0,'rock-4','','','rock-4@51reboot.com',0,1,'2017-08-13 03:34:33.415419'),(8,'pbkdf2_sha256$36000$4KDFO5g58bLR$yv3cvGz7JMiSwABxWlqr2lnlkiQVNTVjDpjugmMwPp8=',NULL,0,'rock-5','','','rock-5@51reboot.com',0,1,'2017-08-13 03:34:33.487916'),(9,'pbkdf2_sha256$36000$jxaxplaDHwuj$gAMjL9nQMk0pN1l4LVNJ0Mdtcj7oBlTthizd4m7Ijv4=',NULL,0,'rock-6','','','rock-6@51reboot.com',0,1,'2017-08-13 03:34:33.567832'),(10,'pbkdf2_sha256$36000$XBUx4PGBcSt3$rEaxGf96LWCte3aQ5cJ4TZ5hdooOyhbhoK1pfEBTb3o=','2017-09-03 07:42:57.215656',0,'rock-7','','','rock-7@51reboot.com',0,1,'2017-08-13 03:34:33.644767'),(11,'pbkdf2_sha256$36000$7EwFLSy9c64a$2rmH7qhPs8S5T/k5inlQ5HQ+IKjrVZ8Td+rfeFfiGMM=',NULL,0,'rock-8','','','rock-8@51reboot.com',0,1,'2017-08-13 03:34:33.726477'),(12,'pbkdf2_sha256$36000$NFZ5kymEVwFq$yyNmGm1reJc8d4xEpj2dr8wH1jwuoIGJ7NUCirJ8Tt4=',NULL,0,'rock-9','','','rock-9@51reboot.com',0,1,'2017-08-13 03:34:33.806381'),(13,'pbkdf2_sha256$36000$mwBVHY10dpFd$quddkl7CnQuyNSe6yhuZc5pq9tDItj7y0hW6VRQXNf8=','2017-08-27 07:42:39.320191',0,'rock-10','','','rock-10@51reboot.com',0,0,'2017-08-13 03:34:33.881853'),(14,'pbkdf2_sha256$36000$U8fayg6CE7v9$hwK+LvvhzDI7prFUk+nuSv0X4I+rAk5g8DZ+kPh3Bdg=',NULL,0,'rock-11','','','rock-11@51reboot.com',0,1,'2017-08-13 03:34:33.954471'),(15,'pbkdf2_sha256$36000$dW50fR2zBsqN$fl+H+Zx+6XfMOkVSxq/zE6rBGJ9GUq1Y5Jy8Bh3gXEQ=',NULL,0,'rock-12','','','rock-12@51reboot.com',0,1,'2017-08-13 03:34:34.030856'),(16,'pbkdf2_sha256$36000$K0QjYhqkfCni$0FYTIVwKNKCGGqqLO2zj7ln/CPs0eIjr0wVfo7GBFNs=',NULL,0,'rock-13','','','rock-13@51reboot.com',0,1,'2017-08-13 03:34:34.108943'),(17,'pbkdf2_sha256$36000$d3ERfhAiXfhu$1Y6VK9e3WEGPNVUSdYaHcpHT/8KfwbnUj1QRx8UKVZI=',NULL,0,'rock-14','','','rock-14@51reboot.com',0,1,'2017-08-13 03:34:34.190907'),(18,'pbkdf2_sha256$36000$WJ5e0XAYENao$0CXVtv8Oq2EimvrNyamv70ajgeUST44zPfhzg7i+YKg=',NULL,0,'rock-15','','','rock-15@51reboot.com',0,1,'2017-08-13 03:34:34.270828'),(19,'pbkdf2_sha256$36000$kUo8ChNSJRWV$v8RR9hDrD302p69RCQjnwgpYnb3P25D7CqIRSlKtsJI=',NULL,0,'rock-16','','','rock-16@51reboot.com',0,1,'2017-08-13 03:34:34.353867'),(20,'pbkdf2_sha256$36000$IhfYFYN0czBn$v1CfvZ0hgfEoCTSuidmYLcaEKGJXaPlkW/QkGLoVO4Q=',NULL,0,'rock-17','','','rock-17@51reboot.com',0,1,'2017-08-13 03:34:34.444937'),(21,'pbkdf2_sha256$36000$8kThYJjcgK15$p1nMdiscS76Q0oCojEjxV1irH2JRlKa/r9Z9RmXcYn0=',NULL,0,'rock-18','','','rock-18@51reboot.com',0,1,'2017-08-13 03:34:34.533953'),(22,'pbkdf2_sha256$36000$sYVlunWki5J3$eeeKkII36Hn65bRQEnqWi13XNd5Od9OKYzoA0fJDJeM=',NULL,0,'rock-19','','','rock-19@51reboot.com',0,1,'2017-08-13 03:34:34.614500'),(23,'pbkdf2_sha256$36000$JN7fiCixOacW$r3BOgRmO3M4QVkoYTajke0gSOoV35nri08sxJV73hE4=',NULL,0,'rock-20','','','rock-20@51reboot.com',0,1,'2017-08-13 03:34:34.698127'),(24,'pbkdf2_sha256$36000$zUFRlQrp53eV$klc/MmMlkHGG/nINJs7Fz3MIVXfRvTKH8qp+gjgd+J4=',NULL,0,'rock-21','','','rock-21@51reboot.com',0,1,'2017-08-13 03:34:34.779987'),(25,'pbkdf2_sha256$36000$arh83Ste5xEO$njtGIGFq11lZgxDyBHcCjZ/LivNwtUf6FEs4/3D7ToM=',NULL,0,'rock-22','','','rock-22@51reboot.com',0,1,'2017-08-13 03:34:34.869133'),(26,'pbkdf2_sha256$36000$UWUMG0QBS2rt$/+/Bfc+goShAjWFpiRMRb3xVnagWyhRWSnU545D+KrI=',NULL,0,'rock-23','','','rock-23@51reboot.com',0,1,'2017-08-13 03:34:34.948579'),(27,'pbkdf2_sha256$36000$ywdImEvJQbk9$QkZLwcFZr+N/ZdYU2LlsqALH/ShnriUhguhWp2+I/Vs=',NULL,0,'rock-24','','','rock-24@51reboot.com',0,1,'2017-08-13 03:34:35.026618'),(28,'pbkdf2_sha256$36000$rYFbOxL4bQs5$68mj46D3JAUMpqHP4VWvaYvIxHMOTkm9PMVykEwMeeo=',NULL,0,'rock-25','','','rock-25@51reboot.com',0,1,'2017-08-13 03:34:35.105248'),(29,'pbkdf2_sha256$36000$4ureGRutjoKy$0AXzgda12RGTyhv/AvaFA2lItQKUDtj4EV4ccsaIDJw=',NULL,0,'rock-26','','','rock-26@51reboot.com',0,1,'2017-08-13 03:34:35.189528'),(30,'pbkdf2_sha256$36000$DSAUQxYGihhb$9lxtgL2dY9f8LAUKL3GAMLX8BuyCBLcf5OViu8yVwYw=',NULL,0,'rock-27','','','rock-27@51reboot.com',0,1,'2017-08-13 03:34:35.280061'),(31,'pbkdf2_sha256$36000$rIqhKTQ9IX9f$BdFJOQ+WL4J2czuYMgFhcKB+Gkb8c/85rt3JIcquPXs=',NULL,0,'rock-28','','','rock-28@51reboot.com',0,1,'2017-08-13 03:34:35.353127'),(32,'pbkdf2_sha256$36000$HghyXFqqLqjH$d68rowh8Cyt3peCV67hUc2N6CJDsVyv0Rj72rUOk7ls=',NULL,0,'rock-29','','','rock-29@51reboot.com',0,1,'2017-08-13 03:34:35.444549'),(33,'pbkdf2_sha256$36000$d4Fu5EikTs7f$P2ZNMH4ntus736fNKbNfRIRIr9QyVyR/GBNL7BuSUXY=',NULL,0,'rock-30','','','rock-30@51reboot.com',0,1,'2017-08-13 03:34:35.518778'),(34,'pbkdf2_sha256$36000$dojiC42I7mBn$MDdcuSklSGKafz2aHWYsTaNLAct/ODvAbAaM6Oe+QYc=',NULL,0,'rock-31','','','rock-31@51reboot.com',0,1,'2017-08-13 03:34:35.595555'),(35,'pbkdf2_sha256$36000$nqriPCTWs1SQ$+FFjVu/b6ySktWZezlyr6vAextyZ40absgvn5i84pLM=',NULL,0,'rock-32','','','rock-32@51reboot.com',0,1,'2017-08-13 03:34:35.682171'),(36,'pbkdf2_sha256$36000$cGiNkqgBj7kX$79pEIAR6lhah6AoqkJyQVwisPwHBmBORMnuSBbk1Pug=',NULL,0,'rock-33','','','rock-33@51reboot.com',0,1,'2017-08-13 03:34:35.760619'),(37,'pbkdf2_sha256$36000$q8jG12jeJDMO$HUH3zBVOuYRD9JEeWij+3eKQildYPpmMbDhcwSyzNIs=',NULL,0,'rock-34','','','rock-34@51reboot.com',0,1,'2017-08-13 03:34:35.836226'),(38,'pbkdf2_sha256$36000$bqiVhjR9ai9M$vDKm1O7mkqkTeJsub30H0/NIW+1hNRAR474QRePUxFE=',NULL,0,'rock-35','','','rock-35@51reboot.com',0,1,'2017-08-13 03:34:35.912713'),(39,'pbkdf2_sha256$36000$MbS5wd6IhmdT$96js2d8CWDMZSq7LP0qOfnJEndWVRYa7TuuwNkTF0po=',NULL,0,'rock-36','','','rock-36@51reboot.com',0,1,'2017-08-13 03:34:35.989799'),(40,'pbkdf2_sha256$36000$Kq0xFviwZPii$YX4CaMBHY3xRxFH3RxShlDw4H15Nio+1aqwvlV6aYeE=',NULL,0,'rock-37','','','rock-37@51reboot.com',0,1,'2017-08-13 03:34:36.067755'),(41,'pbkdf2_sha256$36000$zdFkkINbLN6q$PqoHoazbMFBbeVksbIMOPFr5j+hoCWqDtMdYv72NAIE=',NULL,0,'rock-38','','','rock-38@51reboot.com',0,1,'2017-08-13 03:34:36.142215'),(42,'pbkdf2_sha256$36000$6zf93Pfo2ZDC$iz7ptB1LHEvUJlJW2pVsw2vXCsT6H5Vn2W6iIy7Exac=',NULL,0,'rock-39','','','rock-39@51reboot.com',0,1,'2017-08-13 03:34:36.217542'),(43,'pbkdf2_sha256$36000$lu7r5XI6kLOy$+5Q06qa1kOmrQM4ogJ0/q1fFzjefbxuF6o2BOukYmJM=',NULL,0,'rock-40','','','rock-40@51reboot.com',0,1,'2017-08-13 03:34:36.296870'),(44,'pbkdf2_sha256$36000$RngGSMsIEuDT$krfnQ+01VwMFdyfZto+OhB33xGC/0NlrrzjQwTejIdc=',NULL,0,'rock-41','','','rock-41@51reboot.com',0,1,'2017-08-13 03:34:36.387144'),(45,'pbkdf2_sha256$36000$0LeBHdfzmw5X$OyR1EisnCJTCgS233Sk7ntXu/UKaEgLofhNPrydFwO0=',NULL,0,'rock-42','','','rock-42@51reboot.com',0,1,'2017-08-13 03:34:36.633379'),(46,'pbkdf2_sha256$36000$iqBuw8RmzobY$WUG/BKT8xXPUFI31RJlZlB6+Y/H5iuiV3gUQdPfAICk=',NULL,0,'rock-43','','','rock-43@51reboot.com',0,1,'2017-08-13 03:34:36.758972'),(47,'pbkdf2_sha256$36000$ZjuOr7zdt137$q3AztQxFgU3d9cPfRp5BoIEeP0YJHRUm/zqc3Y+lLzg=',NULL,0,'rock-44','','','rock-44@51reboot.com',0,1,'2017-08-13 03:34:36.913806'),(48,'pbkdf2_sha256$36000$DgTVSll849b0$kQEWt3Y4eYgkwCg6HVQivkrPtE7xUtHVNAXKfuBs3y0=',NULL,0,'rock-45','','','rock-45@51reboot.com',0,1,'2017-08-13 03:34:37.084903'),(49,'pbkdf2_sha256$36000$RALjfdiVQPWs$EICmFNjOF5iMikyDwDco8Brj99uMrGZPjdHp1VV0PRI=',NULL,0,'rock-46','','','rock-46@51reboot.com',0,1,'2017-08-13 03:34:37.244004'),(50,'pbkdf2_sha256$36000$UuVpkPamd7pc$pnBaI7v3JEfXtzhzNvUfSvsAoJxhBGDlRBawYW/1drk=',NULL,0,'rock-47','','','rock-47@51reboot.com',0,1,'2017-08-13 03:34:37.353337'),(51,'pbkdf2_sha256$36000$ZxovC5JHeiHa$HXoUheD9m9YhdEfwB81uRBOcDPU2TpykTTBjmIXeZjA=',NULL,0,'rock-48','','','rock-48@51reboot.com',0,1,'2017-08-13 03:34:37.516869'),(52,'pbkdf2_sha256$36000$AQoI9LjDyFif$ZrDPZ0+aDsqW1F4AT6JhRX5n/AHRfkU+bsusmscluPg=',NULL,0,'rock-49','','','rock-49@51reboot.com',0,1,'2017-08-13 03:34:37.756044'),(53,'pbkdf2_sha256$36000$nBDiCdH2qBNt$08STGtMd7vdgD49FMekat7OkxeJkO09ugPTTR5owFsw=',NULL,0,'rock-50','','','rock-50@51reboot.com',0,1,'2017-08-13 03:34:37.864607'),(54,'pbkdf2_sha256$36000$svLX3mAga4ld$gHYUJlGO34KxYfkyZi/FMmJ/wHloxLxUz+DoYabJzOQ=',NULL,0,'rock-51','','','rock-51@51reboot.com',0,1,'2017-08-13 03:34:37.939441'),(55,'pbkdf2_sha256$36000$67tC1edaScKB$VO1it8XR8pr/pRuRbR83W1ywHZyQIYwYvKEP4fPqOyo=',NULL,0,'rock-52','','','rock-52@51reboot.com',0,1,'2017-08-13 03:34:38.014980'),(56,'pbkdf2_sha256$36000$JP8DBqqhfqAJ$yKHkE21tKuof4pmBMJYLwa21MSoWMplTNHt8av1loXg=',NULL,0,'rock-53','','','rock-53@51reboot.com',0,1,'2017-08-13 03:34:38.093873'),(57,'pbkdf2_sha256$36000$j2agdiORwByv$7ajehNRkVm84jHRcJCLOW2uEkjkeM2Bmpq7w1ZVqBa4=',NULL,0,'rock-54','','','rock-54@51reboot.com',0,1,'2017-08-13 03:34:38.178090'),(58,'pbkdf2_sha256$36000$t1bHX8niQg5E$8b27fCY27xakoyYdSVjPFe1oAnfEbh1xiyuXM06zdko=',NULL,0,'rock-55','','','rock-55@51reboot.com',0,1,'2017-08-13 03:34:38.264549'),(59,'pbkdf2_sha256$36000$qFjrHe1CnvtJ$G1AGe+6xAppnoWFDfi6UBynX4DGdlSNLpjBdxlqflJ0=',NULL,0,'rock-56','','','rock-56@51reboot.com',0,1,'2017-08-13 03:34:38.356060'),(60,'pbkdf2_sha256$36000$FF9L7MwAPmw8$1/BqwTj11DkFzKdQTE/kWYBx+RGwnwvVblW3/eNkCW8=',NULL,0,'rock-57','','','rock-57@51reboot.com',0,1,'2017-08-13 03:34:38.435079'),(61,'pbkdf2_sha256$36000$nUMfSBXqweNv$KAIM+3hlOcgF/7akqyE5IuCNokEgf7MXh3mAvstZ4YI=',NULL,0,'rock-58','','','rock-58@51reboot.com',0,1,'2017-08-13 03:34:38.542536'),(62,'pbkdf2_sha256$36000$BTECJTBZLzmz$snpw35/+3Dzg92NOrST/l4Zx0botGUw0IKuCzCJlM0k=',NULL,0,'rock-59','','','rock-59@51reboot.com',0,1,'2017-08-13 03:34:38.627132'),(63,'pbkdf2_sha256$36000$0lTQKJOQ0lDY$BaMnuIpjPf+JqGQ5W+9YSwS9HBG7frNEVJMz8y1y/Xo=',NULL,0,'rock-60','','','rock-60@51reboot.com',0,1,'2017-08-13 03:34:38.708670'),(64,'pbkdf2_sha256$36000$Xp7z6YxyT0uj$GQ4EydCoteSpMzb207oAvNdf6mQdP0xKZqIN48MtrpU=',NULL,0,'rock-61','','','rock-61@51reboot.com',0,1,'2017-08-13 03:34:38.791593'),(65,'pbkdf2_sha256$36000$CY25qn0LinGn$lRAAXL405xKEz747K07kMv16Cmr2/z+a2na6pDYGU2o=',NULL,0,'rock-62','','','rock-62@51reboot.com',0,1,'2017-08-13 03:34:38.882482'),(66,'pbkdf2_sha256$36000$NZQsHhfw4LZC$XR9KHGewmbMoTKfpyqoauIaF2cojn82LmVE74LZ3oOU=',NULL,0,'rock-63','','','rock-63@51reboot.com',0,1,'2017-08-13 03:34:38.968102'),(67,'pbkdf2_sha256$36000$jcF2sEPGGHAo$KfOl1c+9dPwlM2ydknZ2e4QvgHqC47TdLaojvd8Joz0=',NULL,0,'rock-64','','','rock-64@51reboot.com',0,1,'2017-08-13 03:34:39.049255'),(68,'pbkdf2_sha256$36000$NrGNuZO36ihc$DXh25GQ01y3XIoJuT/mRB2MILwRKEnij/+R5/VEPLBg=',NULL,0,'rock-65','','','rock-65@51reboot.com',0,1,'2017-08-13 03:34:39.131168'),(69,'pbkdf2_sha256$36000$uQu13uFaWZyI$CmQwbU0Wo/8HXqAhTz8ryCH14kKT+qfqoBuQxKcGhK0=',NULL,0,'rock-66','','','rock-66@51reboot.com',0,0,'2017-08-13 03:34:39.205759'),(70,'pbkdf2_sha256$36000$hMHFZ4mQW68W$TTdQx3saGJIUaDLeaF+fBkUN0+r/eHontfTfIZmOxPA=',NULL,0,'rock-67','','','rock-67@51reboot.com',0,1,'2017-08-13 03:34:39.294713'),(71,'pbkdf2_sha256$36000$Ck3Uu6XqtT6Q$JJJwNupX1MW1gIwqo+Mk51pJCPZRgl5NibcnZ1W6HII=',NULL,0,'rock-68','','','rock-68@51reboot.com',0,0,'2017-08-13 03:34:39.371554'),(72,'pbkdf2_sha256$36000$es9hRmRmdre2$U2PV7U2StLvFPzAx3pyLaHgo70Nfe87KDlGmEQ9l4tc=',NULL,0,'rock-69','','','rock-69@51reboot.com',0,1,'2017-08-13 03:34:39.445598'),(73,'pbkdf2_sha256$36000$1JaEECrJXkCU$veGi6G0j4wFeJ+LeLSHGnSV7YP/57w20Kfa6LNY+sb8=',NULL,0,'rock-70','','','rock-70@51reboot.com',0,1,'2017-08-13 03:34:39.528534'),(74,'pbkdf2_sha256$36000$NbWciWmWytly$WyFJcuD3xyeAYliNTU+IA2qBibzaqYKnmP6EYWmkgh8=',NULL,0,'rock-71','','','rock-71@51reboot.com',0,1,'2017-08-13 03:34:39.613752'),(75,'pbkdf2_sha256$36000$y1dnPZOd8vzG$tmxmalxgJ/hctVOZXjezpVxDMW4Hy5DP4y22FhuqibI=',NULL,0,'rock-72','','','rock-72@51reboot.com',0,1,'2017-08-13 03:34:39.690755'),(76,'pbkdf2_sha256$36000$imUQjRRtq67W$Rmx3VUPcf+CWM6E2783wZu++gKHO6ijQf/3D05RyGHU=',NULL,0,'rock-73','','','rock-73@51reboot.com',0,1,'2017-08-13 03:34:39.765655'),(77,'pbkdf2_sha256$36000$iHySBRslnIwG$1TNi5TUc6eu8kjb7uCtV8LpwJ7aVkbPuGCEsQHi8IHc=',NULL,0,'rock-74','','','rock-74@51reboot.com',0,1,'2017-08-13 03:34:39.842265'),(78,'pbkdf2_sha256$36000$If3ClmkfgLRD$0XR2OzzavlwhQ+jMSxnoqs7nlMku197/Dmftz3n27SI=',NULL,0,'rock-75','','','rock-75@51reboot.com',0,1,'2017-08-13 03:34:39.920771'),(79,'pbkdf2_sha256$36000$oOOnwmqaHtsp$10CrXOCPdb9NR2JQkbMtB0vTynWhF3fQfIruLF73Iqs=',NULL,0,'rock-76','','','rock-76@51reboot.com',0,1,'2017-08-13 03:34:40.012730'),(80,'pbkdf2_sha256$36000$COFt8uuUG4An$BOD4SE/uKFRtIIwoGlpQfAKALboQxfN0Ll1bAJ7irXE=',NULL,0,'rock-77','','','rock-77@51reboot.com',0,1,'2017-08-13 03:34:40.094728'),(81,'pbkdf2_sha256$36000$IkVZhH7L7CTS$u+esWgcGrruc0k85+9+q9EBlEStTToRWSDuYZ9mtOyw=',NULL,0,'rock-78','','','rock-78@51reboot.com',0,1,'2017-08-13 03:34:40.174235'),(82,'pbkdf2_sha256$36000$IjS9715w3DzR$Dd7bIgZ5lzrxWaKcrj6KvgQbt7zoEppXbEX6nRE8VQI=',NULL,0,'rock-79','','','rock-79@51reboot.com',0,1,'2017-08-13 03:34:40.251429'),(83,'pbkdf2_sha256$36000$ccNVL85AYLwL$49m8ZtbhOuDb/jD9SGaJrxYYVA8le06Mt/qJRN47HZY=',NULL,0,'rock-80','','','rock-80@51reboot.com',0,1,'2017-08-13 03:34:40.336416'),(84,'pbkdf2_sha256$36000$YxrwfRSP8gSE$WrKAJRKnGSZRCrrGs/TXh3lJbQnI636XpWuoxoxczkA=',NULL,0,'rock-81','','','rock-81@51reboot.com',0,1,'2017-08-13 03:34:40.419662'),(85,'pbkdf2_sha256$36000$paPvVrCVOSU5$e7z4AoAcMFalZOzsl8qCtNn/d8KTODkIaKFM7LGt3y4=',NULL,0,'rock-82','','','rock-82@51reboot.com',0,1,'2017-08-13 03:34:40.498910'),(86,'pbkdf2_sha256$36000$VcpGZBkk4pNp$2sGwtCCPS3ez55cDopk3GNrTm+VV7EuSipolepCCE/g=',NULL,0,'rock-83','','','rock-83@51reboot.com',0,1,'2017-08-13 03:34:40.590295'),(87,'pbkdf2_sha256$36000$JN37Pdfytz6E$o6MjULGDlPs7UakLDGCCL8bnbLJhQZd8xhyoLOsbxP8=',NULL,0,'rock-84','','','rock-84@51reboot.com',0,1,'2017-08-13 03:34:40.679772'),(88,'pbkdf2_sha256$36000$fbr4DTuQXjNm$NDmJlWfX27H6WBwmb85WnyqdwqCj8FAz5aWhek23Frs=',NULL,0,'rock-85','','','rock-85@51reboot.com',0,1,'2017-08-13 03:34:40.757825'),(89,'pbkdf2_sha256$36000$4FZE1nSgMjlI$GOQ4IUx0iF874WcXLG9YbBWpsvMRaZKw+3M3whmWHt0=',NULL,0,'rock-86','','','rock-86@51reboot.com',0,1,'2017-08-13 03:34:40.830921'),(90,'pbkdf2_sha256$36000$Ing8IK5GJ9Hw$KGpMxehyoXtYkZo3T583gKJLPp5IgHAD/JCtllmZPeI=',NULL,0,'rock-87','','','rock-87@51reboot.com',0,1,'2017-08-13 03:34:40.904656'),(91,'pbkdf2_sha256$36000$DJhFsy5tOdSO$5FjczlElth3lU0nPxFm1q4kOCsQeDcG9z6k1yDVmREY=',NULL,0,'rock-88','','','rock-88@51reboot.com',0,1,'2017-08-13 03:34:40.988871'),(92,'pbkdf2_sha256$36000$jMrJcANSlTuv$2nj0MX91StxroswM3CiO+o5hvSCB5ZIEdunYb0/iLcA=',NULL,0,'rock-89','','','rock-89@51reboot.com',0,1,'2017-08-13 03:34:41.062430'),(93,'pbkdf2_sha256$36000$VHHLZvaPTTyt$IfTVpX47NHG6Ao7eNVIXf9Ds9fHSh5S1G+i4f1amaAc=',NULL,0,'rock-90','','','rock-90@51reboot.com',0,1,'2017-08-13 03:34:41.140847'),(94,'pbkdf2_sha256$36000$hr18KEM9p8js$f+4dh3XDAWWyr1JPEUAaToEiB4774pnct8rkxqPGZ68=',NULL,0,'rock-91','','','rock-91@51reboot.com',0,1,'2017-08-13 03:34:41.219456'),(95,'pbkdf2_sha256$36000$bRxCgVmVcgxi$oLACuY7rKGwYD7ULeoYviuR4CNFRycFONtbxLX0wSAM=',NULL,0,'rock-92','','','rock-92@51reboot.com',0,1,'2017-08-13 03:34:41.301834'),(96,'pbkdf2_sha256$36000$Zi0UD9SaN9DA$++SGJl5JUPqy+ghImgRsIOvi7CCaGgbVfTc3hxj4IiI=',NULL,0,'rock-93','','','rock-93@51reboot.com',0,1,'2017-08-13 03:34:41.386577'),(97,'pbkdf2_sha256$36000$INC9irLYwmCV$ktqKcsbQHBz9+N/aydzfijbTvQmlHcEV2HAhOx/InuU=',NULL,0,'rock-94','','','rock-94@51reboot.com',0,1,'2017-08-13 03:34:41.460278'),(98,'pbkdf2_sha256$36000$qLh9cHnsK990$oLhOukqBqxvKiZK+y1TwSK+j3hHK5OCOa/mImAOC7Zk=',NULL,0,'rock-95','','','rock-95@51reboot.com',0,1,'2017-08-13 03:34:41.540549'),(99,'pbkdf2_sha256$36000$cj1T7BSQ6r7e$/uBxPqGYqdqJyBejOqRfiQOYXRXbY4iwkPNoCHnsAyM=',NULL,0,'rock-96','','','rock-96@51reboot.com',0,1,'2017-08-13 03:34:41.632552'),(100,'pbkdf2_sha256$36000$lAcEnBAX0YDc$sG3Wy47d+0BVPHJBQRv6FAd4lK8eNCHbj0kn98GUnvk=',NULL,0,'rock-97','','','rock-97@51reboot.com',0,1,'2017-08-13 03:34:41.714595'),(101,'pbkdf2_sha256$36000$s0BZEvJGFW1K$IQXQEbRjj3b7RwM971wy8XHeyT9+ou2mejSjvsR/lI8=',NULL,0,'rock-98','','','rock-98@51reboot.com',0,1,'2017-08-13 03:34:41.791051'),(102,'pbkdf2_sha256$36000$GIhSWlm53b8H$cPnj5uVXAdJ4UUf7Udo12yRwWqrsVKlvCui6hiqqVIE=',NULL,0,'rock-99','','','rock-99@51reboot.com',0,0,'2017-08-13 03:34:41.864773'),(103,'pbkdf2_sha256$36000$OAjEtV5KX5oa$eccAjjfhiUWRb/agR2rIatpdgrkyxNxMVYbwuQHxp30=',NULL,1,'admin','','','admin@163.com',1,1,'2017-08-20 03:00:26.690160'),(104,'pbkdf2_sha256$36000$YShjERDqEvY4$S+dPfQgoRFTyh4+mBDMLphi9YTTF5H4BEsGd1CuB6ew=',NULL,0,'tom1','','','tom1@126.com',0,1,'2017-08-27 08:58:54.752707'),(105,'pbkdf2_sha256$36000$Ty744bnHjOyY$Jso2o6+IzvyujCsem113YYeCP7uBXTCXZTfyz34/2gA=',NULL,0,'tom2','','','tom2@126.com',0,1,'2017-08-27 08:58:54.953707'),(106,'pbkdf2_sha256$36000$eQ1fZhHEF13T$wtyzDeumqAek0baoLz3zAd567tp80dOXuL8DWdrSIrg=',NULL,0,'tom3','','','tom3@126.com',0,1,'2017-08-27 08:58:55.034093'),(107,'pbkdf2_sha256$36000$BR4EvkKZnQEU$SShWi3b94phazxb9Zp/xZT+hjQwLsSx7NywrGWxZPEo=',NULL,0,'tom4','','','tom4@126.com',0,1,'2017-08-27 08:58:55.108510'),(108,'pbkdf2_sha256$36000$3nTUKaL5uZ42$sIjUQwgoXo0uG2qRG6izsXrtpIzTPJW7OxShbRq/jd8=',NULL,0,'zhang1','','','zhang1@126.com',0,1,'2017-08-27 08:59:40.156239'),(109,'pbkdf2_sha256$36000$ekDarpQ68m51$kL6GiL2dmdnXnQD9ihU1OdRSaJmSCjDr+bAhy1ZX5Cc=',NULL,0,'zhang2','','','zhang2@126.com',0,1,'2017-08-27 08:59:40.250301'),(110,'pbkdf2_sha256$36000$qbtwck3f4DDH$TZOhb3U0OOC3WcUb6FpIdop6u+pLOgUhspm+HPGTNZE=',NULL,0,'zhang3','','','zhang3@126.com',0,1,'2017-08-27 08:59:40.470387'),(111,'pbkdf2_sha256$36000$kjwSLc31Iw8L$zCaijn0hCY7O6lV0VKgst6Y4PWuO6HbUK8O5mPCwJEw=',NULL,0,'zhang4','','','zhang4@126.com',0,1,'2017-08-27 08:59:40.566836'),(112,'pbkdf2_sha256$36000$WN5E1XsIRDMy$l31L5KFrllms+7hD+btH0F3Z47S+fugwmAv/xUWQ+Uo=','2017-09-03 09:52:28.748051',1,'reboot','','','reboot@123.com',1,1,'2017-09-03 07:51:14.741896');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (15,4,5),(13,7,1),(5,7,3),(8,8,1),(7,10,1),(10,10,5);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'dashboard','person'),(8,'resources','idc'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-08-06 07:56:39.549860'),(2,'auth','0001_initial','2017-08-06 07:56:42.460677'),(3,'admin','0001_initial','2017-08-06 07:56:42.985750'),(4,'admin','0002_logentry_remove_auto_add','2017-08-06 07:56:43.043368'),(5,'contenttypes','0002_remove_content_type_name','2017-08-06 07:56:43.401386'),(6,'auth','0002_alter_permission_name_max_length','2017-08-06 07:56:43.604429'),(7,'auth','0003_alter_user_email_max_length','2017-08-06 07:56:43.827810'),(8,'auth','0004_alter_user_username_opts','2017-08-06 07:56:43.855497'),(9,'auth','0005_alter_user_last_login_null','2017-08-06 07:56:44.459077'),(10,'auth','0006_require_contenttypes_0002','2017-08-06 07:56:44.471504'),(11,'auth','0007_alter_validators_add_error_messages','2017-08-06 07:56:44.503577'),(12,'auth','0008_alter_user_username_max_length','2017-08-06 07:56:44.691009'),(13,'sessions','0001_initial','2017-08-06 07:56:44.901153'),(14,'dashboard','0001_initial','2017-08-27 03:32:29.150037'),(15,'dashboard','0002_auto_20170827_0339','2017-08-27 03:39:55.900258'),(16,'dashboard','0003_delete_person','2017-08-27 05:52:13.413144'),(17,'resources','0001_initial','2017-08-27 05:52:29.282523'),(18,'resources','0002_auto_20170903_0902','2017-09-03 09:02:36.220137');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('5hrvvw1f5bds1geoqkxxujsc30kuom1e','MmE3MDcyYzdlMjUxYjY2NzBmYzg1YzBjNDQ4ZWJiMjcyZjJlOTg0Yzp7Il9hdXRoX3VzZXJfaWQiOiIxMTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjM1OTE0OTYwZTIyOWZmNDMwNzA4ZGNkM2EwOTMyYzg2NWViOGMxYjMifQ==','2017-09-17 09:52:28.758618'),('7av3zrhrth11zbe4n2eeu3424vpqvrq7','NTc3NTk2YTU1ZWQxOGUwZTEyMjUzYTI1Y2UxZWMzNTYxMTQxZTIwMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2YjYxN2FlN2FkNjEwZWJmZmYwNTAyMWEyZDM3ODAxMzgxN2QxZmY5In0=','2017-09-03 06:41:44.952303'),('cios2c1d4b8w8mpu3la5t64s4h9b5t8y','NTc3NTk2YTU1ZWQxOGUwZTEyMjUzYTI1Y2UxZWMzNTYxMTQxZTIwMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2YjYxN2FlN2FkNjEwZWJmZmYwNTAyMWEyZDM3ODAxMzgxN2QxZmY5In0=','2017-09-10 08:56:32.271592'),('dz6p4uu3ddli4911owbuv81ysrpreayj','NTc3NTk2YTU1ZWQxOGUwZTEyMjUzYTI1Y2UxZWMzNTYxMTQxZTIwMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2YjYxN2FlN2FkNjEwZWJmZmYwNTAyMWEyZDM3ODAxMzgxN2QxZmY5In0=','2017-09-03 03:54:59.049723'),('evsk8x0f2bmmipl22l6zvtjr212mcfq0','NTc3NTk2YTU1ZWQxOGUwZTEyMjUzYTI1Y2UxZWMzNTYxMTQxZTIwMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2YjYxN2FlN2FkNjEwZWJmZmYwNTAyMWEyZDM3ODAxMzgxN2QxZmY5In0=','2017-09-03 08:27:40.826741'),('o5wiaxgds9nbxgqphxapulqmltdk7qul','NTc3NTk2YTU1ZWQxOGUwZTEyMjUzYTI1Y2UxZWMzNTYxMTQxZTIwMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2YjYxN2FlN2FkNjEwZWJmZmYwNTAyMWEyZDM3ODAxMzgxN2QxZmY5In0=','2017-09-04 13:57:43.150361'),('s40jvmse8sekqxsqefimfdmkcshj7nt3','NTc3NTk2YTU1ZWQxOGUwZTEyMjUzYTI1Y2UxZWMzNTYxMTQxZTIwMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2YjYxN2FlN2FkNjEwZWJmZmYwNTAyMWEyZDM3ODAxMzgxN2QxZmY5In0=','2017-09-17 08:38:10.899266'),('ujvju0jpmlhg58496hvzhdulcajx8p05','NTc3NTk2YTU1ZWQxOGUwZTEyMjUzYTI1Y2UxZWMzNTYxMTQxZTIwMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2YjYxN2FlN2FkNjEwZWJmZmYwNTAyMWEyZDM3ODAxMzgxN2QxZmY5In0=','2017-09-10 07:43:49.059148'),('wciea83338v5trp3zfjwmtxexvez4com','NTc3NTk2YTU1ZWQxOGUwZTEyMjUzYTI1Y2UxZWMzNTYxMTQxZTIwMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2YjYxN2FlN2FkNjEwZWJmZmYwNTAyMWEyZDM3ODAxMzgxN2QxZmY5In0=','2017-09-03 07:07:38.649844');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resources_idc`
--

DROP TABLE IF EXISTS `resources_idc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resources_idc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `idc_name` varchar(100) NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `username` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resources_idc`
--

LOCK TABLES `resources_idc` WRITE;
/*!40000 ALTER TABLE `resources_idc` DISABLE KEYS */;
INSERT INTO `resources_idc` VALUES (1,'jxq','酒仙桥机房','北京酒仙桥','12345678','rock@51reboot','rock'),(2,'zw','北京兆维','北京兆维联通机房','12345678','zw@163.com','tom'),(3,'yz','亦庄机房','北京大兴','12345678','jack@51reboot','jack'),(22,'afe','rear','rear','','re','rear');
/*!40000 ALTER TABLE `resources_idc` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-04 22:29:46
