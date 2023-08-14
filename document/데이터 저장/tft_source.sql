-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema TFT_SOURCE
-- -----------------------------------------------------
-- utf8mb4_general_ci

-- -----------------------------------------------------
-- Schema TFT_SOURCE
--
-- utf8mb4_general_ci
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `TFT_SOURCE` DEFAULT CHARACTER SET utf8mb4 ;
USE `TFT_SOURCE` ;

-- -----------------------------------------------------
-- Table `TFT_SOURCE`.`match`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFT_SOURCE`.`match` ;

CREATE TABLE IF NOT EXISTS `TFT_SOURCE`.`match` (
  `match_id` VARCHAR(20) NOT NULL,
  `match_date` DATETIME NULL,
  `match_length` DECIMAL(6,2) NULL,
  `version_major` SMALLINT NOT NULL,
  `version_minor` SMALLINT NOT NULL,
  `version_patch` SMALLINT NOT NULL,
  `version_date` DATETIME NOT NULL,
  `tft_set_number` TINYINT NULL,
  PRIMARY KEY (`match_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TFT_SOURCE`.`player`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFT_SOURCE`.`player` ;

CREATE TABLE IF NOT EXISTS `TFT_SOURCE`.`player` (
  `puuid` VARCHAR(80) NOT NULL,
  `name` VARCHAR(40) NULL,
  `continent` VARCHAR(20) NOT NULL,
  `region` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`puuid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TFT_SOURCE`.`match_player`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFT_SOURCE`.`match_player` ;

CREATE TABLE IF NOT EXISTS `TFT_SOURCE`.`match_player` (
  `match_player_id` VARCHAR(20) NOT NULL,
  `match_id` VARCHAR(20) NOT NULL,
  `puuid` VARCHAR(80) NOT NULL,
  `last_round` TINYINT NULL,
  `level` TINYINT NULL,
  `placement` TINYINT NOT NULL,
  `time_eliminated` DECIMAL(6,2) NULL,
  PRIMARY KEY (`match_player_id`),
  CONSTRAINT `fk_match_player_match`
    FOREIGN KEY (`match_id`)
    REFERENCES `TFT_SOURCE`.`match` (`match_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_player_player1`
    FOREIGN KEY (`puuid`)
    REFERENCES `TFT_SOURCE`.`player` (`puuid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_match_player_match_idx` ON `TFT_SOURCE`.`match_player` (`match_id` ASC) VISIBLE;

CREATE INDEX `fk_match_player_player1_idx` ON `TFT_SOURCE`.`match_player` (`puuid` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `TFT_SOURCE`.`match_augment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFT_SOURCE`.`match_augment` ;

CREATE TABLE IF NOT EXISTS `TFT_SOURCE`.`match_augment` (
  `match_player_id` VARCHAR(20) NOT NULL,
  `sequence` INT NOT NULL,
  `name` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`match_player_id`, `sequence`),
  CONSTRAINT `fk_match_augment_match_player1`
    FOREIGN KEY (`match_player_id`)
    REFERENCES `TFT_SOURCE`.`match_player` (`match_player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TFT_SOURCE`.`match_trait`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFT_SOURCE`.`match_trait` ;

CREATE TABLE IF NOT EXISTS `TFT_SOURCE`.`match_trait` (
  `match_player_id` VARCHAR(20) NOT NULL,
  `sequence` INT NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  `num_units` SMALLINT NOT NULL,
  `style` TINYINT NOT NULL,
  `tier_current` TINYINT NOT NULL,
  `tier_total` TINYINT NOT NULL,
  PRIMARY KEY (`match_player_id`, `sequence`),
  CONSTRAINT `fk_match_trait_match_player1`
    FOREIGN KEY (`match_player_id`)
    REFERENCES `TFT_SOURCE`.`match_player` (`match_player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TFT_SOURCE`.`match_unit`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFT_SOURCE`.`match_unit` ;

CREATE TABLE IF NOT EXISTS `TFT_SOURCE`.`match_unit` (
  `match_player_id` VARCHAR(20) NOT NULL,
  `sequence` INT NOT NULL,
  `name` VARCHAR(40) NOT NULL,
  `rarity` TINYINT NOT NULL,
  `tier` TINYINT NOT NULL,
  `item1` VARCHAR(60) NULL,
  `item2` VARCHAR(60) NULL,
  `item3` VARCHAR(60) NULL,
  PRIMARY KEY (`match_player_id`, `sequence`),
  CONSTRAINT `fk_match_unit_match_player1`
    FOREIGN KEY (`match_player_id`)
    REFERENCES `TFT_SOURCE`.`match_player` (`match_player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TFT_SOURCE`.`player_statistic`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFT_SOURCE`.`player_statistic` ;

CREATE TABLE IF NOT EXISTS `TFT_SOURCE`.`player_statistic` (
  `puuid` VARCHAR(80) NOT NULL,
  `ranking` TINYINT NOT NULL,
  `league_point` SMALLINT NULL,
  `wins` SMALLINT NULL,
  `losses` SMALLINT NULL,
  `update_date` DATETIME NOT NULL,
  PRIMARY KEY (`puuid`, `update_date`),
  CONSTRAINT `fk_player_statistic_player1`
    FOREIGN KEY (`puuid`)
    REFERENCES `TFT_SOURCE`.`player` (`puuid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
