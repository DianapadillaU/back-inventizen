/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `db_inventory` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `db_inventory`;

CREATE TABLE IF NOT EXISTS `categorias` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre_categoria` varchar(50) NOT NULL DEFAULT '0',
  `codigo_unico` varchar(50) NOT NULL DEFAULT '0',
  `imagen` longblob NOT NULL,
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `codigo_unico` (`codigo_unico`),
  KEY `nombre_categoria` (`nombre_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `inventario` (
  `id_inventario` int NOT NULL AUTO_INCREMENT,
  `codigo_unico` int NOT NULL DEFAULT '0',
  `producto` varchar(50) NOT NULL DEFAULT '0',
  `categoria` varchar(50) NOT NULL DEFAULT '0',
  `precio_costo` int NOT NULL DEFAULT '0',
  `precio_venta` int NOT NULL DEFAULT '0',
  `stock_ideal` int NOT NULL DEFAULT '0',
  `descripcion` varchar(300) DEFAULT '0',
  PRIMARY KEY (`id_inventario`),
  UNIQUE KEY `codigo_unico` (`codigo_unico`),
  KEY `categoria` (`categoria`),
  CONSTRAINT `FK_inventario_categorias` FOREIGN KEY (`categoria`) REFERENCES `categorias` (`nombre_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(50) NOT NULL DEFAULT '0',
  `cate_producto` varchar(50) NOT NULL DEFAULT '0',
  `serial_producto` int DEFAULT NULL,
  `stock_producto` int DEFAULT NULL,
  `precio_IVA` int DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  UNIQUE KEY `serial_producto` (`serial_producto`),
  KEY `cate_producto` (`cate_producto`),
  CONSTRAINT `FK_productos_categorias` FOREIGN KEY (`cate_producto`) REFERENCES `categorias` (`nombre_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `proveedores` (
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre_proveedor` varchar(50) NOT NULL DEFAULT '0',
  `codigo_unico` varchar(50) DEFAULT '0',
  `telefono` int NOT NULL DEFAULT '0',
  `direccion` varchar(50) NOT NULL DEFAULT '0',
  `ciudad` varchar(50) NOT NULL DEFAULT '0',
  `correo` varchar(100) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_proveedor`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `codigo_unico` (`codigo_unico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(50) DEFAULT NULL,
  `pass` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
