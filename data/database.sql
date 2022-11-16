-- Adminer 4.7.1 MySQL dump

SET NAMES utf8;
SET time_zone = '-03:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;


USE movimentacoes_processuais;

DROP TABLE IF EXISTS `processos`;
CREATE TABLE IF NOT EXISTS `processos` (
  `id_processo` int(11) NOT NULL AUTO_INCREMENT,
  `processo` varchar(25) NOT NULL,
  `ultima_atualizacao` date DEFAULT NULL,
  `uf` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id_processo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `movimentacoes`;
CREATE TABLE IF NOT EXISTS `movimentacoes` (
  `id_movimentacao` int(11) NOT NULL AUTO_INCREMENT,
  `id_processo` int(11) NOT NULL,
  `movimentacao` text NOT NULL,
  `data_movimentacao` datetime DEFAULT NULL,
  PRIMARY KEY (`id_movimentacao`),
  KEY `id_processo` (`id_processo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
ALTER TABLE `movimentacoes`
  ADD CONSTRAINT `movimentacoes_ibfk_1` FOREIGN KEY (`id_processo`) REFERENCES `processos` (`id_processo`);
