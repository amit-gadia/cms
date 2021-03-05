CREATE TABLE `addmission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `frname` varchar(50) DEFAULT NULL,
  `lname` varchar(50) DEFAULT NULL,
  `dob` varchar(50) DEFAULT NULL,
  `f_name` varchar(50) DEFAULT NULL,
  `f_occ` varchar(50) DEFAULT NULL,
  `m_name` varchar(50) DEFAULT NULL,
  `m_occ` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `mob_no` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `aadhar` varchar(50) DEFAULT NULL,
  `course` varchar(50) DEFAULT NULL,
  `branch` varchar(50) DEFAULT NULL,
  `bg` varchar(50) DEFAULT NULL,
  `reg_no` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `assign` (
  `id` int NOT NULL AUTO_INCREMENT,
  `class` varchar(50) DEFAULT NULL,
  `file` varchar(50) DEFAULT NULL,
  `stu_id` varchar(50) DEFAULT NULL,
  `assign_id` varchar(50) DEFAULT NULL,
  `abc` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `assignment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(50) DEFAULT NULL,
  `tname` varchar(50) DEFAULT NULL,
  `sname` varchar(50) DEFAULT NULL,
  `duedate` varchar(50) DEFAULT NULL,
  `note` varchar(50) DEFAULT NULL,
  `a` varchar(50) DEFAULT NULL,
  `fc_code` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `attendance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `class` varchar(50) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `sub` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `stuid` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `branch` (
  `id` int NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(50) DEFAULT NULL,
  `branch_fees` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ;
CREATE TABLE `calendar` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_name` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `category_event` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `code` (
  `id` int NOT NULL AUTO_INCREMENT,
  `branch` varchar(50) DEFAULT NULL,
  `course` varchar(50) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `faculty` (
  `id` int NOT NULL AUTO_INCREMENT,
  `frname` varchar(50) DEFAULT NULL,
  `lname` varchar(50) DEFAULT NULL,
  `dob` varchar(50) DEFAULT NULL,
  `bsd` varchar(50) DEFAULT NULL,
  `msd` varchar(50) DEFAULT NULL,
  `fname` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `Blood_group` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `number` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `fees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stu_id` varchar(50) DEFAULT NULL,
  `fees_details` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `fees_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(50) DEFAULT NULL,
  `fees` varchar(50) DEFAULT NULL,
  `course_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `hostel_room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_no` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `fees` varchar(50) DEFAULT NULL,
  `stu_id` varchar(50) DEFAULT NULL,
  `local_guardian` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `goods_detailsM_P_E` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `library` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stu_id` varchar(50) DEFAULT NULL,
  `book_id` varchar(50) DEFAULT NULL,
  `issue_date` varchar(50) DEFAULT NULL,
  `submit_date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `mess` (
  `id` int NOT NULL AUTO_INCREMENT,
  `schedule` varchar(50) DEFAULT NULL,
  `timing` varchar(50) DEFAULT NULL,
  `menu` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `mess_emp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mess_emmp_id` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `number` varchar(50) DEFAULT NULL,
  `dest` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `notice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `details` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `room_no` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_no` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `route` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bus_no` varchar(50) DEFAULT NULL,
  `pick_pt` varchar(50) DEFAULT NULL,
  `fees` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `route_bus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bus_no` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `subject` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sub_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `timetable` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sub_name` varchar(50) DEFAULT NULL,
  `fac_name` varchar(50) DEFAULT NULL,
  `ab` varchar(50) DEFAULT NULL,
  `classcode` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `transport_bus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `BUS_NUMBER` varchar(50) DEFAULT NULL,
  `PICK_UP` varchar(50) DEFAULT NULL,
  `STUDENT_ID` varchar(50) DEFAULT NULL,
  `NAME` varchar(50) DEFAULT NULL,
  `FEES` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `passwd` varchar(50) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);



--------------------------------------------------------------------------------------------------------------------------------




CREATE TABLE `warden` (
  `id` int NOT NULL AUTO_INCREMENT,
  `warden_id` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `number` varchar(50) DEFAULT NULL,
  `dest` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `transport_fees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stu_id` varchar(50) DEFAULT NULL,
  `fees_details` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `hostel_fees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stu_id` varchar(50) DEFAULT NULL,
  `fees_details` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
