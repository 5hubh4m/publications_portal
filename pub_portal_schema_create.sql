-- -----------------------------------------------------
-- Schema pub_portal
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `pub_portal` ;

-- -----------------------------------------------------
-- Schema pub_portal
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pub_portal` DEFAULT CHARACTER SET utf8 ;
USE `pub_portal` ;

-- -----------------------------------------------------
-- Table `pub_portal`.`publisher`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`publisher` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`publisher` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `type` ENUM('Journal', 'Conference', 'Publishing House') NOT NULL,
  `url` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `url_UNIQUE` (`url` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pub_portal`.`institute`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`institute` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`institute` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `city` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  `postal_code` DECIMAL(10,0) NULL,
  `url` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `institute_id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `url_UNIQUE` (`url` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pub_portal`.`department`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`department` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`department` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pub_portal`.`author`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`author` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`author` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `middle_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `url` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `institute.id` INT NULL,
  `department.id` INT NULL,
  `type` ENUM('Faculty', 'Student') NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_author_institute1_idx` (`institute.id` ASC),
  INDEX `fk_author_department1_idx` (`department.id` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  UNIQUE INDEX `url_UNIQUE` (`url` ASC),
  CONSTRAINT `fk_author_institute1`
    FOREIGN KEY (`institute.id`)
    REFERENCES `pub_portal`.`institute` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_author_department1`
    FOREIGN KEY (`department.id`)
    REFERENCES `pub_portal`.`department` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pub_portal`.`publication`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`publication` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`publication` (
  `id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT(512) NOT NULL,
  `url` VARCHAR(255) NULL,
  `location` VARCHAR(45) NULL,
  `date` DATE NOT NULL,
  `publication_code` VARCHAR(255) NULL,
  `publisher.id` INT NOT NULL,
  `approved_by` INT NULL,
  `approved` TINYINT(1) NOT NULL,
  `submitted_by` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_publication_publisher_idx` (`publisher.id` ASC),
  UNIQUE INDEX `publication_code_UNIQUE` (`publication_code` ASC),
  UNIQUE INDEX `url_UNIQUE` (`url` ASC),
  INDEX `fk_publication_author1_idx` (`approved_by` ASC),
  INDEX `fk_publication_author2_idx` (`submitted_by` ASC),
  CONSTRAINT `fk_publication_publisher`
    FOREIGN KEY (`publisher.id`)
    REFERENCES `pub_portal`.`publisher` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_publication_author1`
    FOREIGN KEY (`approved_by`)
    REFERENCES `pub_portal`.`author` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_publication_author2`
    FOREIGN KEY (`submitted_by`)
    REFERENCES `pub_portal`.`author` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pub_portal`.`publication_has_author`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`publication_has_author` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`publication_has_author` (
  `publication.id` INT NOT NULL,
  `author.id` INT NOT NULL,
  `degree` ENUM('first', 'second', 'third', 'corresponding', 'other') NOT NULL,
  PRIMARY KEY (`publication.id`, `author.id`),
  INDEX `fk_publication_has_author_author1_idx` (`author.id` ASC),
  INDEX `fk_publication_has_author_publication1_idx` (`publication.id` ASC),
  CONSTRAINT `fk_publication_has_author_publication1`
    FOREIGN KEY (`publication.id`)
    REFERENCES `pub_portal`.`publication` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_publication_has_author_author1`
    FOREIGN KEY (`author.id`)
    REFERENCES `pub_portal`.`author` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pub_portal`.`publication_field`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`publication_field` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`publication_field` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pub_portal`.`publication_has_field`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`publication_has_field` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`publication_has_field` (
  `publication.id` INT NOT NULL,
  `field.id` INT NOT NULL,
  PRIMARY KEY (`publication.id`, `field.id`),
  INDEX `fk_publication_has_publication_field_publication_field1_idx` (`field.id` ASC),
  INDEX `fk_publication_has_publication_field_publication1_idx` (`publication.id` ASC),
  CONSTRAINT `fk_publication_has_publication_field_publication1`
    FOREIGN KEY (`publication.id`)
    REFERENCES `pub_portal`.`publication` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_publication_has_publication_field_publication_field1`
    FOREIGN KEY (`field.id`)
    REFERENCES `pub_portal`.`publication_field` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pub_portal`.`field_has_department`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`field_has_department` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`field_has_department` (
  `field.id` INT NOT NULL,
  `department.id` INT NOT NULL,
  PRIMARY KEY (`field.id`, `department.id`),
  INDEX `fk_publication_field_has_department_department1_idx` (`department.id` ASC),
  INDEX `fk_publication_field_has_department_publication_field1_idx` (`field.id` ASC),
  CONSTRAINT `fk_publication_field_has_department_publication_field1`
    FOREIGN KEY (`field.id`)
    REFERENCES `pub_portal`.`publication_field` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_publication_field_has_department_department1`
    FOREIGN KEY (`department.id`)
    REFERENCES `pub_portal`.`department` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pub_portal`.`author_has_qualification`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pub_portal`.`author_has_qualification` ;

CREATE TABLE IF NOT EXISTS `pub_portal`.`author_has_qualification` (
  `qualification` ENUM('B. Tech.', 'B. S.', 'M. Tech.', 'M. S.', 'Ph. D.') NOT NULL,
  `author.id` INT NOT NULL,
  INDEX `fk_author_qualification_author1_idx` (`author.id` ASC),
  PRIMARY KEY (`qualification`, `author.id`),
  CONSTRAINT `fk_author_qualification_author1`
    FOREIGN KEY (`author.id`)
    REFERENCES `pub_portal`.`author` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Users `pub_portal`
-- -----------------------------------------------------
DROP USER admin;
CREATE USER 'admin' IDENTIFIED BY 'admin_passwd';
GRANT CREATE, DROP, GRANT OPTION, REFERENCES, ALTER, DELETE, INDEX, INSERT, SELECT, UPDATE, TRIGGER ON TABLE pub_portal.* TO 'admin';
GRANT ALL ON TABLE pub_portal.* TO 'admin';

DROP USER faculty;
CREATE USER 'faculty' IDENTIFIED BY 'faculty_passwd';
GRANT SELECT, INSERT, UPDATE, SELECT ON TABLE `pub_portal`.* TO 'faculty';

DROP USER student;
CREATE USER 'student' IDENTIFIED BY 'student_passwd';
GRANT SELECT, INSERT, UPDATE, SELECT ON TABLE `pub_portal`.* TO 'faculty';

DROP USER viewer;
CREATE USER 'viewer';
GRANT SELECT ON TABLE pub_portal.* TO 'viewer';

-- -----------------------------------------------------
-- Trigger `pub_portal`.`publication`
-- -----------------------------------------------------
USE `pub_portal`;

DELIMITER $$

USE `pub_portal`$$
DROP TRIGGER IF EXISTS `pub_portal`.`publication_BEFORE_INSERT` $$
USE `pub_portal`$$
CREATE DEFINER = CURRENT_USER TRIGGER `pub_portal`.`publication_BEFORE_INSERT` BEFORE INSERT ON `publication` FOR EACH ROW
BEGIN
    IF NEW.`submitted_by` IN (SELECT `id` FROM `author` WHERE `type` = 'Student') AND (NEW.`approved` = True OR NEW.`approved_by` <> NULL) 
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Students can\'t create approved publications.';
    END IF;
END;$$


USE `pub_portal`$$
DROP TRIGGER IF EXISTS `pub_portal`.`publication_BEFORE_UPDATE` $$
USE `pub_portal`$$
CREATE DEFINER = CURRENT_USER TRIGGER `pub_portal`.`publication_BEFORE_UPDATE` BEFORE UPDATE ON `publication` FOR EACH ROW
BEGIN
	IF NEW.`approved_by` IN (SELECT `id` FROM `author` WHERE `type` = 'Student') 
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Students can\'t approve publications.';
    END IF;
END$$


DELIMITER ;
