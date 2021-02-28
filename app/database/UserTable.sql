CREATE TABLE `users` (
	`no` INT(11) NOT NULL AUTO_INCREMENT,
	`status` CHAR(15) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
	`email` CHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
	`pw` TEXT NULL COLLATE 'utf8mb4_bin',
	`name` CHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
	`phone_number` CHAR(20) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
	`profile_img` TEXT NULL COLLATE 'utf8mb4_bin',
	`sns_type` CHAR(5) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
	`marketing_agree` CHAR(1) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
	`created_at` TIMESTAMP NULL DEFAULT NULL,
	`updated_at` TIMESTAMP NULL DEFAULT NULL,
	PRIMARY KEY (`no`)
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB
;
