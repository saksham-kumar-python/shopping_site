-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: the_ganges
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `products_info`
--

DROP TABLE IF EXISTS `products_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_info` (
  `product_name` varchar(255) DEFAULT NULL,
  `product_stocks` int DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `price` varchar(255) DEFAULT NULL,
  `product_detail` text,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_info`
--

LOCK TABLES `products_info` WRITE;
/*!40000 ALTER TABLE `products_info` DISABLE KEYS */;
INSERT INTO `products_info` VALUES ('Coca Cola',1200,'coke.jpg','35','All over the world, Coca-Cola is synonymous with happiness and celebration. A coke (as it is affectionately called) is the first thing that comes to the mind of millions across the globe when they reach out for a cold drink. Coca-Cola has a truly remarkable heritage. From a humble beginning in 1886, it\'s now the flagship brand of the largest manufacturer, marketer and distributor of non-alcoholic beverages in the world. In India though, it has not just become a market leader, but has become a phenomenon, an obsession even, with people. It has ceased to remain just a refreshing cold drink, rather, becoming a part of every household. Any occasion, any celebration, you will find a coke right there, adding to the happiness. The brand recognition that coca cola enjoys is second to none. All this has been possible due to Coca-Cola\'s commitment to give the consumer, the very best experience possible. Every coke you consume comes with the same refreshing taste and the promise of quality and trust. All the ingredients used to make this flavourful and refreshing drink are 100 % natural, safe and go through a strict quality control programme in advanced manufacturing facilities.',1),('Mcvities Digestive',1760,'digestive.jpg','20','McVities Digestives biscuits - Light can be enjoyed as part of a healthy diet and lifestyle. It contains 70 percent wholemeal and wheat goodness. Good source of fibre.',2),('HP Folio 9470m',34,'hp_folio.jpg','80000','Elevate your business with an ultrathin, professional laptop that empowers users to perform at their very best. Enterprise-class features, comprehensive security, and a refined collaboration experience handle even the most demanding tasks with streamlined efficiency.',3),('HP X3000',134,'hp3000.jpg','2500','Built with strict standards and guidelines, the HP Mouse X3000 effortlessly blends sleek, modern design with life-enhancing, advanced features. 70 years experience. Strict quality control. 1 of the world\'s leading notebook manufacturers. HP delivers cutting-edge products built with some of the industry\'s toughest standards to enhance the way you connect and communicate. The sleek and modern HP Mouse X3000 adds an instant touch of trend-setting style to any work space. Glossy black and metallic gray shine with sophistication. Plus, its curvy silhouette gives it a seductive shape. The HP Wireless Mouse X3000 features the latest technology you crave. 2.4GHz wireless connection sets you free. Battery life lasts 12 months.(1) Scroll wheel flies through the web and documents. Optical sensor works on most surfaces.',4),('Lays Classic',1500,'lays_classic.jpg','20','Always fresh tasting, crispy and delicious, each bag of Lay\'s Classic® potato chips is made with specially selected potatoes and to the highest quality standards. Crispy and light tasting, Lay\'s Classic® potato chips were designed to put a smile on everyone\'s face, which makes them the perfect snack to share',5),('Maggi Pack of 1',1100,'maggi.jpg','15','Maggi is a product that belongs to Nestle India, which is one of the leading fast food companies in the country. ... Maggi is a product of Nestlé India, a subsidiary of Nestlé of Switzerland. Major Maggi products that are manufactured by Nestlé include instant noodles, stocks, instant soups and ketchup',6),('3x3 Rubik\'s Cube',600,'rubik.jpg','70','This 3x3x3 magic cube, featuring tripod base with V.I.A6688 logo will be an excellent pick as a stress reliever game. It weighs about 120 grams. It further improves intelligence quotient, hand-eye coordination and concentration.',7),('Wilson Ultra 100',55,'Wilson_Ultra100.jpeg','17000','This 25 inch model inspired by roger Federer is suitable for juniors aged 8 to 10. Its light weight makes for an easy swinging racquet.',8),('Yeet Buzzer',69,'yeet.jpg','500','Yeet Buzzer inspired by Lazarbeam is a fun toy for kids of all age groups',9),('Babolat Pure Aero Drive',34,'babolat.jpg','21000','The pure aero represents a significant improvement over the previous generation of aero racquets: A new aerodynamic frame enables the racquet head to move more quickly and thereby increases ball speed, while new FSI spin technology provides enhanced lift. This racquet responds superbly to players who seek power and optimal spin, like Rafael Nadal and jo-Wilfried Tsonga. Babolat is a French tennis, badminton and squash equipment company, headquartered in Lyon, best known for its high quality strings, tennis racquets and tennis accessories which are used by several top players. The company has made strings since 1875, when Pierre Babolat created the first strings made of natural gut. Babolat continued to focus on strings until 1994, when it became a total tennis company, producing also racquet frames and selling them in Europe. It then expanded sales to japan and later to the USA in 2000. Sales of Babolat racquets increased rapidly in north America, Europe and Asia. Babolat is also a pioneer in connected sport technology and launched a connected tennis racquet in 2014 and a connected wrist-worn tennis wearable with piq in 2015. Right now product line of Babolat includes racquets, strings, accessories, balls, bags etc. Which are having huge global demand because of its high quality and performance.',10),('Limca (250mL)',1000,'limca.jpg','35','Limca is a lemon- and lime-flavoured carbonated soft drink made primarily in India and certain parts of the U.S. It contains 60 calories per 150ml can. The formula does not include fruit, relying instead on artificial flavours.',11),('Lays Cream',2000,'lays_cream.jpeg','20','It all starts with farm-grown potatoes, cooked and seasoned to perfection. Then we add the tang of sour cream and mild onions. So every LAY\'S® cream potato chips is perfectly crispy and delicious. Happiness in Every Bite.®',12),('The Grail A190C Guitar',200,'guitar.jpg','17000','The Grail A190C proves that a 39” guitar can look snazzy and sound good. Its cutaway design makes it the most contemporary in its class. Right from the abalone like inlays to the fan pick guard; this guitar has all the features that will make you want to own it. The A190C is made of basswood with a glossy lacquer finish and ABS binding. It has individual machine heads for stable tuning. This is the perfect guitar for students who want a convenient size without compromising on design and sound. Designed in Taiwan, grailguitars.com are becoming the leading choice for quality guitars at an affordable cost.',13);
/*!40000 ALTER TABLE `products_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_status`
--

DROP TABLE IF EXISTS `transaction_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_status` (
  `user_id` int NOT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `current_status` varchar(255) DEFAULT NULL,
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `address` text,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_status`
--

LOCK TABLES `transaction_status` WRITE;
/*!40000 ALTER TABLE `transaction_status` DISABLE KEYS */;
INSERT INTO `transaction_status` VALUES (2,12,4,'C',46,'2020-03-30 11:12:59',NULL),(2,4,3,'C',48,'2020-03-30 11:13:14',NULL),(2,13,1,'C',49,'2020-03-30 11:13:29',NULL),(4,8,1,'DELIVERED',74,'2020-04-06 12:42:51',NULL),(4,6,1,'DELIVERED',76,'2020-04-06 13:26:49',NULL),(4,1,1,'DELIVERED',77,'2020-04-06 13:26:59',NULL),(4,1,1,'DELIVERED',78,'2020-04-06 13:30:07',NULL),(4,7,4,'DELIVERED',79,'2020-04-06 13:31:16',NULL),(4,10,1,'DELIVERED',80,'2020-04-06 13:31:45',NULL),(4,1,12,'DELIVERED',82,'2020-04-16 20:22:14',NULL),(4,2,6,'C',85,'2020-04-16 20:37:29',NULL),(5,1,1,'DELIVERED',87,'2020-04-16 20:39:54',NULL),(4,6,5,'C',88,'2020-05-18 09:39:42',NULL),(4,7,1,'C',89,'2020-05-18 09:40:09',NULL);
/*!40000 ALTER TABLE `transaction_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_info`
--

DROP TABLE IF EXISTS `users_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_info` (
  `first_name` varchar(255) DEFAULT NULL,
  `second_name` varchar(255) DEFAULT NULL,
  `phone_no` bigint DEFAULT NULL,
  `points` int DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `if_signed_in` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_info`
--

LOCK TABLES `users_info` WRITE;
/*!40000 ALTER TABLE `users_info` DISABLE KEYS */;
INSERT INTO `users_info` VALUES ('Saksham','Kumar',9990881097,NULL,'KumarSaksham','Morley',1,0),('Aadish','Saini',9990221923,NULL,'SainiAadish','jajwut',2,0),('Anil','Kumar',9911725618,400,'a','a',4,1),('s','s',1234567891,NULL,'s','s',5,0);
/*!40000 ALTER TABLE `users_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-18 19:22:48
