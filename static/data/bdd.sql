-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema demt1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema demt1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `demt1` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `demt1` ;

-- -----------------------------------------------------
-- Table `demt1`.`direction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`direction` (
  `id_direction` INT NOT NULL,
  `nom_direction` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_direction`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`bureau`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`bureau` (
  `id_bureau` INT NOT NULL,
  `nom_bureau` VARCHAR(100) NOT NULL,
  `id_direction` INT NOT NULL,
  PRIMARY KEY (`id_bureau`),
  INDEX `id_direction` (`id_direction` ASC) VISIBLE,
  CONSTRAINT `bureau_ibfk_1`
    FOREIGN KEY (`id_direction`)
    REFERENCES `demt1`.`direction` (`id_direction`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`chapitre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`chapitre` (
  `id_chapitre` INT NOT NULL,
  `nom` VARCHAR(100) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `engagement` DOUBLE NULL DEFAULT '0',
  `montant_initiale` DOUBLE NOT NULL,
  `mondatement` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`id_chapitre`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`projet`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`projet` (
  `id_projet` INT NOT NULL,
  `nom_projet` VARCHAR(100) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `date_debut` DATE NOT NULL,
  `date_fin` DATE NOT NULL,
  `id_bureau` INT NOT NULL,
  `chapitre_id_chapitre` INT NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `montant` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`id_projet`, `chapitre_id_chapitre`),
  INDEX `id_bureau` (`id_bureau` ASC) VISIBLE,
  INDEX `chapitre_id_chapitre` (`chapitre_id_chapitre` ASC) VISIBLE,
  CONSTRAINT `projet_ibfk_1`
    FOREIGN KEY (`id_bureau`)
    REFERENCES `demt1`.`bureau` (`id_bureau`),
  CONSTRAINT `projet_ibfk_2`
    FOREIGN KEY (`chapitre_id_chapitre`)
    REFERENCES `demt1`.`chapitre` (`id_chapitre`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`achat_sur_facture`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`achat_sur_facture` (
  `id_facture` VARCHAR(45) NOT NULL,
  `montant` DOUBLE NOT NULL,
  `date` DATE NOT NULL,
  `projet_id_projet` INT NOT NULL,
  `id_fournisseur` INT NOT NULL,
  `devise` ENUM('DZD', 'EURO', 'DOLLAR') NULL DEFAULT NULL,
  `etat` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_facture`),
  INDEX `projet_id_projet` (`projet_id_projet` ASC) VISIBLE,
  INDEX `fk_achat_sur_facture_fournisseur1_idx` (`id_fournisseur` ASC) VISIBLE,
  CONSTRAINT `achat_sur_facture_ibfk_1`
    FOREIGN KEY (`projet_id_projet`)
    REFERENCES `demt1`.`projet` (`id_projet`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`agent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`agent` (
  `id_agent` INT NOT NULL,
  `nom` VARCHAR(100) NOT NULL,
  `prenom` VARCHAR(100) NOT NULL,
  `role` ENUM('directeur', 'chef direction', 'chef bureau', 'agent') NOT NULL,
  `direction_id_direction` INT NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `bureau_id_bureau` INT NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_agent`, `bureau_id_bureau`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  INDEX `fk_agent_direction1` (`direction_id_direction` ASC) VISIBLE,
  INDEX `fk_agent_bureau1_idx` (`bureau_id_bureau` ASC) VISIBLE,
  CONSTRAINT `fk_agent_direction1`
    FOREIGN KEY (`direction_id_direction`)
    REFERENCES `demt1`.`direction` (`id_direction`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`bon_de_commande`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`bon_de_commande` (
  `id_bon` INT NOT NULL,
  `date_bon` DATE NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `montant` DOUBLE NOT NULL,
  `etat` VARCHAR(50) NOT NULL,
  `date_de_notification` DATE NULL DEFAULT NULL,
  `delais` INT NOT NULL,
  `agent_id_agent` INT NOT NULL,
  `id_contrat` VARCHAR(45) NULL DEFAULT NULL,
  `id_facture` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_bon`),
  INDEX `agent_id_agent` (`agent_id_agent` ASC) VISIBLE,
  INDEX `fk_bon_de_commande_contract1_idx` (`id_contrat` ASC) VISIBLE,
  INDEX `fk_bon_de_commande_achat_sur_facture1_idx` (`id_facture` ASC) VISIBLE,
  CONSTRAINT `bon_de_commande_ibfk_2`
    FOREIGN KEY (`agent_id_agent`)
    REFERENCES `demt1`.`agent` (`id_agent`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`fournisseur`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`fournisseur` (
  `id_fournisseur` INT NOT NULL,
  `nom` VARCHAR(100) NOT NULL,
  `adresse` TEXT NULL DEFAULT NULL,
  `contact` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id_fournisseur`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`contract`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`contract` (
  `id_contrat` VARCHAR(45) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `date_debut` DATE NOT NULL,
  `date_de_notification` DATE NULL DEFAULT NULL,
  `min` DOUBLE NOT NULL,
  `max` DOUBLE NULL DEFAULT NULL,
  `duree` INT NOT NULL,
  `id_projet` INT NOT NULL,
  `id_fournisseur` INT NOT NULL,
  `devise` ENUM('DZD', 'DOLLAR', 'EURO') NOT NULL,
  `type` ENUM('ferme', 'commande') NOT NULL,
  `engagement` DOUBLE NULL DEFAULT '0',
  `projet_id_projet` INT NOT NULL,
  `projet_chapitre_id_chapitre` INT NOT NULL,
  `etat` ENUM('engagement', 'instance engagé') NULL DEFAULT NULL,
  PRIMARY KEY (`id_projet`, `id_fournisseur`, `id_contrat`),
  INDEX `id_fournisseur` (`id_fournisseur` ASC) VISIBLE,
  INDEX `fk_contract_projet1_idx` (`projet_id_projet` ASC, `projet_chapitre_id_chapitre` ASC) VISIBLE,
  CONSTRAINT `contract_ibfk_2`
    FOREIGN KEY (`id_fournisseur`)
    REFERENCES `demt1`.`fournisseur` (`id_fournisseur`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`historique_etat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`historique_etat` (
  `id_historique` INT NOT NULL,
  `id_projet` INT NULL DEFAULT NULL,
  `etat` VARCHAR(45) NOT NULL,
  `date_debut` DATE NOT NULL,
  `date_fin` DATE NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `agent_id_agent` INT NOT NULL,
  `id_facture` VARCHAR(45) NULL DEFAULT NULL,
  `id_contrat` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_historique`),
  INDEX `id_projet` (`id_projet` ASC) VISIBLE,
  INDEX `agent_id_agent` (`agent_id_agent` ASC) VISIBLE,
  INDEX `fk_historique_etat_achat_sur_facture1_idx` (`id_facture` ASC) VISIBLE,
  INDEX `fk_historique_etat_contract1_idx` (`id_contrat` ASC) VISIBLE,
  CONSTRAINT `historique_etat_ibfk_2`
    FOREIGN KEY (`agent_id_agent`)
    REFERENCES `demt1`.`agent` (`id_agent`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`pv_de_reception`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`pv_de_reception` (
  `id_PV` VARCHAR(45) NOT NULL,
  `date` DATE NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `id_bon` INT NOT NULL,
  `agent_id_agent` INT NOT NULL,
  `date_facture` DATE NULL DEFAULT NULL,
  `montant` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`id_PV`, `id_bon`, `agent_id_agent`),
  INDEX `id_bon` (`id_bon` ASC) VISIBLE,
  INDEX `agent_id_agent` (`agent_id_agent` ASC) VISIBLE,
  CONSTRAINT `pv_de_reception_ibfk_1`
    FOREIGN KEY (`id_bon`)
    REFERENCES `demt1`.`bon_de_commande` (`id_bon`),
  CONSTRAINT `pv_de_reception_ibfk_2`
    FOREIGN KEY (`agent_id_agent`)
    REFERENCES `demt1`.`agent` (`id_agent`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `demt1`.`pv_de_reception_difinitive`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `demt1`.`pv_de_reception_difinitive` (
  `id_pv_de_rec_difinitive` VARCHAR(45) NOT NULL,
  `date_etablissement` DATE NOT NULL,
  `contract_id_projet` INT NOT NULL,
  `contract_id_fournisseur` INT NOT NULL,
  `contract_id_contract` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_pv_de_rec_difinitive`, `contract_id_projet`, `contract_id_fournisseur`, `contract_id_contract`),
  INDEX `contract_id_projet` (`contract_id_projet` ASC, `contract_id_fournisseur` ASC, `contract_id_contract` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

USE `demt1` ;

-- -----------------------------------------------------
-- procedure truncate_all_tables
-- -----------------------------------------------------

DELIMITER $$
USE `demt1`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `truncate_all_tables`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE table_name VARCHAR(255);
    DECLARE table_cursor CURSOR FOR 
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = DATABASE();
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN table_cursor;
    
    read_loop: LOOP
        FETCH table_cursor INTO table_name;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET @sql = CONCAT('TRUNCATE TABLE `', table_name, '`');
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;
    
    CLOSE table_cursor;
END$$

DELIMITER ;
USE `demt1`;

DELIMITER $$
USE `demt1`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `demt1`.`direction_BEFORE_INSERT`
BEFORE INSERT ON `demt1`.`direction`
FOR EACH ROW
BEGIN
DECLARE identifier INT;
    SELECT IFNULL(MAX(id_direction), 0) INTO identifier FROM direction;
    SET NEW.id_direction = identifier + 1;
END$$

USE `demt1`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `demt1`.`bureau_BEFORE_INSERT`
BEFORE INSERT ON `demt1`.`bureau`
FOR EACH ROW
BEGIN
DECLARE identifier INT;
    SELECT IFNULL(MAX(id_bureau), 0) INTO identifier FROM bureau;
    SET NEW.id_bureau = identifier + 1;
END$$

USE `demt1`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `demt1`.`projet_BEFORE_INSERT_date`
BEFORE INSERT ON `demt1`.`projet`
FOR EACH ROW
BEGIN
  IF NEW.date_fin < NEW.date_debut THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'End date cannot be before start date';
  END IF;
END$$

USE `demt1`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `demt1`.`projet_BEFORE_UPDATE`
BEFORE UPDATE ON `demt1`.`projet`
FOR EACH ROW
BEGIN
  IF NEW.date_fin < NEW.date_debut THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'End date cannot be before start date';
  END IF;
END$$

USE `demt1`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `demt1`.`agent_BEFORE_INSERT`
BEFORE INSERT ON `demt1`.`agent`
FOR EACH ROW
BEGIN
    DECLARE identifier INT;
    SELECT IFNULL(MAX(id_agent), 0) INTO identifier FROM agent;
    SET NEW.id_agent = identifier + 1;
END$$

USE `demt1`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `demt1`.`fournisseur_BEFORE_INSERT`
BEFORE INSERT ON `demt1`.`fournisseur`
FOR EACH ROW
BEGIN
DECLARE identifier INT;
    SELECT IFNULL(MAX(id_fournisseur), 0) INTO identifier FROM fournisseur;
    SET NEW.id_fournisseur = identifier + 1;
END$$

USE `demt1`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `demt1`.`contract_BEFORE_INSERT_date`
BEFORE INSERT ON `demt1`.`contract`
FOR EACH ROW
BEGIN
  IF NEW.date_de_notification IS NOT NULL AND NEW.date_de_notification < NEW.date_debut THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Notification date cannot be before start date';
  END IF;

  IF NEW.duree < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Duration cannot be negative';
  END IF;

  IF NEW.max IS NOT NULL AND NEW.max < NEW.min THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Min is greater than Max';
  END IF;
END$$

USE `demt1`$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `demt1`.`historique_etat_BEFORE_INSERT`
BEFORE INSERT ON `demt1`.`historique_etat`
FOR EACH ROW
BEGIN
DECLARE identifier INT;
    SELECT IFNULL(MAX(id_historique), 0) INTO identifier FROM historique_etat;
    SET NEW.id_historique = identifier + 1;
END$$


DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
