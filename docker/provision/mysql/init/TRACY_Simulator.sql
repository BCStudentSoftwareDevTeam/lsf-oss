-- Run the following commands in MySQL to build a simulated Tracy database

CREATE DATABASE IF NOT EXISTS `UTE`;

CREATE TABLE UTE.`STUPOSN` (
	POSN_CODE varchar(24) NULL,
	POSN_TITLE varchar(120) NULL,
	WLS varchar(20) NULL,
	ORG varchar(24) NULL,
	ACCOUNT varchar(24) NULL,
	DEPT_NAME varchar(1000) NULL
);

CREATE TABLE UTE.`STUDATA` (
	PIDM char(8) NULL,
	ID char(36) NULL,
	FIRST_NAME varchar(240) NULL,
	LAST_NAME varchar(240) NULL,
	CLASS_LEVEL varchar(1000) NULL,
	ACADEMIC_FOCUS varchar(68) NULL,
	MAJOR varchar(1000) NULL,
	PROBATION varchar(1000) NULL,
	ADVISOR varchar(484) NULL,
	STU_EMAIL varchar(160) NULL,
	STU_CPO varchar(1000) NULL,
	LAST_POSN varchar(24) NULL,
	LAST_SUP_PIDM varchar(24) NULL
);

CREATE TABLE UTE.`STUSTAFF` (
	PIDM char(8) NULL,
	ID varchar(36) NULL,
	FIRST_NAME varchar(240) NULL,
	LAST_NAME varchar(240) NULL,
	EMAIL varchar(1000) NULL,
	CPO varchar(1000) NULL,
	ORG varchar(24) NULL,
	DEPT_NAME varchar(1000) NULL
);

INSERT INTO UTE.`STUPOSN` (POSN_CODE, POSN_TITLE, WLS, ORG, ACCOUNT, DEPT_NAME)
    VALUES
    ('S12345', 'DUMMY POSITION', '1', '2141', '1234', 'COMPUTER SCIENCE'),
    ('S12346', 'DUMMY POSITION 2', '2', '2141', '1234', 'COMPUTER SCIENCE'),
    ('S12347', 'DUMMY POSITION 3', '3', '2142', '1235', 'NOT COMPUTER SCIENCE'),
    ('S12348', 'DUMMY POSITION 4', '4', '2142', '1235', 'NOT COMPUTER SCIENCE');


 INSERT INTO UTE.`STUSTAFF` (PIDM, ID, FIRST_NAME, LAST_NAME, EMAIL, CPO, ORG, DEPT_NAME)
	VALUES
	('1', 'B00123456', 'Scott', 'Heggen', 'heggens@berea.edu', '2188', '2141', 'COMPUTER SCIENCE'),
	('2', 'B00123457', 'Jan', 'Pearce', 'pearcej@berea.edu', '2189', '2141', 'COMPUTER SCIENCE'),
	('3', 'B00123458', 'Mario', 'Nakazawa', 'nakazawam@berea.edu', '2187', '2142', 'NOT COMPUTER SCIENCE'),
	('4', 'B00123459', 'Emily', 'Lovell', 'lovelle@berea.edu', '2186', '2142', 'NOT COMPUTER SCIENCE');

INSERT INTO UTE.`STUDATA` ( PIDM, ID, FIRST_NAME, LAST_NAME, CLASS_LEVEL,
				ACADEMIC_FOCUS, MAJOR, PROBATION, ADVISOR, STU_EMAIL, STU_CPO, LAST_POSN, LAST_SUP_PIDM)
	VALUES
	('1', 'B12344321', 'Kat', 'Adams', 'Senior', '', 'COMPUTER SCIENCE', 'False', '', 'adamska@berea.edu', '1234', '', ''),
    ('2', 'B12344322', 'May', 'Jue', 'Junior', '', 'COMPUTER SCIENCE', 'False', '', 'juem@berea.edu', '1235', '', ''),
    ('3', 'B12344323', 'Hailey', 'Barnett', 'Sophomore', '', 'NOT COMPUTER SCIENCE', 'False', '', 'barnetth@berea.edu', '1236', '', ''),
    ('4', 'B12344324', 'Guillermo', 'Cruz', 'Freshman', '', 'NOT COMPUTER SCIENCE', 'True', '', 'cruzg@berea.edu', '1237', '', '');
