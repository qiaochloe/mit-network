--Initialize table
CREATE TABLE `mit`.`prerequisites` (
    `course` VARCHAR(45) NOT NULL,
    `prereq` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`course`, `prereq`));

--Add foreign keys
ALTER TABLE `mit`.`prerequisites` 
ADD INDEX `prereq_fk_idx` (`prereq` ASC) VISIBLE;
;
ALTER TABLE `mit`.`prerequisites` 
ADD CONSTRAINT `course_fk`
  FOREIGN KEY (`course`)
  REFERENCES `mit`.`eecs` (`course_code`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `prereq_fk`
  FOREIGN KEY (`prereq`)
  REFERENCES `mit`.`eecs` (`course_code`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;
