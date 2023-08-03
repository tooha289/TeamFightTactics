-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema TFTDB
-- -----------------------------------------------------
-- utf8mb4_general_ci

-- -----------------------------------------------------
-- Schema TFTDB
--
-- utf8mb4_general_ci
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `TFTDB` DEFAULT CHARACTER SET utf8mb4 ;
USE `TFTDB` ;

-- -----------------------------------------------------
-- Table `TFTDB`.`match`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFTDB`.`match` ;

CREATE TABLE IF NOT EXISTS `TFTDB`.`match` (
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
-- Table `TFTDB`.`player`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFTDB`.`player` ;

CREATE TABLE IF NOT EXISTS `TFTDB`.`player` (
  `puuid` VARCHAR(80) NOT NULL,
  `name` VARCHAR(40) NULL,
  `continent` VARCHAR(20) NOT NULL,
  `region` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`puuid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TFTDB`.`match_player`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFTDB`.`match_player` ;

CREATE TABLE IF NOT EXISTS `TFTDB`.`match_player` (
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
    REFERENCES `TFTDB`.`match` (`match_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_player_player1`
    FOREIGN KEY (`puuid`)
    REFERENCES `TFTDB`.`player` (`puuid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_match_player_match_idx` ON `TFTDB`.`match_player` (`match_id` ASC) VISIBLE;

CREATE INDEX `fk_match_player_player1_idx` ON `TFTDB`.`match_player` (`puuid` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `TFTDB`.`match_augment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFTDB`.`match_augment` ;

CREATE TABLE IF NOT EXISTS `TFTDB`.`match_augment` (
  `match_player_id` VARCHAR(20) NOT NULL,
  `sequence` INT NOT NULL,
  `name` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`match_player_id`, `sequence`),
  CONSTRAINT `fk_match_augment_match_player1`
    FOREIGN KEY (`match_player_id`)
    REFERENCES `TFTDB`.`match_player` (`match_player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TFTDB`.`match_trait`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFTDB`.`match_trait` ;

CREATE TABLE IF NOT EXISTS `TFTDB`.`match_trait` (
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
    REFERENCES `TFTDB`.`match_player` (`match_player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TFTDB`.`match_unit`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFTDB`.`match_unit` ;

CREATE TABLE IF NOT EXISTS `TFTDB`.`match_unit` (
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
    REFERENCES `TFTDB`.`match_player` (`match_player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TFTDB`.`player_statistic`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TFTDB`.`player_statistic` ;

CREATE TABLE IF NOT EXISTS `TFTDB`.`player_statistic` (
  `puuid` VARCHAR(80) NOT NULL,
  `ranking` TINYINT NOT NULL,
  `league_point` SMALLINT NULL,
  `wins` SMALLINT NULL,
  `losses` SMALLINT NULL,
  `update_date` DATETIME NOT NULL,
  PRIMARY KEY (`puuid`, `update_date`),
  CONSTRAINT `fk_player_statistic_player1`
    FOREIGN KEY (`puuid`)
    REFERENCES `TFTDB`.`player` (`puuid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
