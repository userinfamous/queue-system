-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 13, 2018 at 02:20 AM
-- Server version: 5.6.34-log
-- PHP Version: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `users`
--

-- --------------------------------------------------------

--
-- Table structure for table `academic_queue`
--

CREATE TABLE `academic_queue` (
  `Number` int(10) NOT NULL,
  `Time_in` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Time_out` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `Time_diff` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `academic_queue`
--

INSERT INTO `academic_queue` (`Number`, `Time_in`, `Time_out`, `Time_diff`) VALUES
(10, '2018-08-11 15:12:16', '2018-08-11 12:55:08', '00:00:04');

-- --------------------------------------------------------

--
-- Table structure for table `accounting_queue`
--

CREATE TABLE `accounting_queue` (
  `Number` int(10) NOT NULL,
  `Time_in` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Time_out` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `Time_diff` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `accounting_queue`
--

INSERT INTO `accounting_queue` (`Number`, `Time_in`, `Time_out`, `Time_diff`) VALUES
(1, '2018-08-10 12:40:07', '2018-08-10 12:41:14', '00:01:07'),
(10, '2018-08-11 12:55:08', '0000-00-00 00:00:00', '00:00:00'),
(19, '2018-08-11 15:55:48', '2018-08-11 15:53:02', '00:00:43');

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `ID` int(11) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Username` varchar(100) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `Department` varchar(30) DEFAULT NULL,
  `People_Served` int(30) DEFAULT NULL,
  `Register_Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`ID`, `Name`, `Email`, `Username`, `Password`, `Department`, `People_Served`, `Register_Date`) VALUES
(1, 'Test1', 'test1@ciaschool.edu.kh', 'acct_1', '$5$rounds=535000$NQpVu2WMeQgVP/vV$sLcvN1C70RYfF0V5.Y4cz2Bb5gabC5gyLS6gm5FFn61', 'Accounting', NULL, '2018-08-10 09:49:46'),
(2, 'test1', 'test1@ciaschool.edu.kh', 'fd_1', '$5$rounds=535000$nra5DFAJ8pz97Z7D$9NOvycsrBTepiM7ZzL/5.x46lz8HcGT0PfzT.DfaKt8', 'Front Desk', NULL, '2018-08-10 09:50:39'),
(3, 'test1', 'test1@ciaschool.edu.kh', 'acd_1', '$5$rounds=535000$b2OsLadBfe9CM7tX$kqu6vL84GxX8KoGxKaQFrYs0bZHIDo0JTs3JI1kkw88', 'Academic', NULL, '2018-08-10 09:51:15');

-- --------------------------------------------------------

--
-- Table structure for table `front_desk_queue`
--

CREATE TABLE `front_desk_queue` (
  `Number` int(10) NOT NULL,
  `Time_in` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Time_out` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `Time_diff` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `front_desk_queue`
--

INSERT INTO `front_desk_queue` (`Number`, `Time_in`, `Time_out`, `Time_diff`) VALUES
(1, '2018-08-10 12:41:14', '2018-08-10 12:41:27', '00:00:13'),
(3, '2018-08-10 12:58:31', '2018-08-10 12:59:22', '00:00:00'),
(4, '2018-08-10 13:05:25', '2018-08-10 14:33:27', '01:28:02'),
(19, '2018-08-11 15:55:39', '0000-00-00 00:00:00', '00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `request_types`
--

CREATE TABLE `request_types` (
  `Department` varchar(20) NOT NULL,
  `Request_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `request_types`
--

INSERT INTO `request_types` (`Department`, `Request_type`) VALUES
('Front Desk', 'Leave Early'),
('Front Desk', 'General Enquiry'),
('Front Desk', 'Enrollment'),
('Accounting', 'Tuition Fee'),
('Accounting', 'Payment'),
('Front Desk', 'Late Slip'),
('Front Desk', 'Reenrollment'),
('Front Desk', 'Lost and Found'),
('Academic', 'Academic Paperwork'),
('Academic', 'Academic Enquiry'),
('Academic', 'Transcript/Report Card'),
('Accounting', 'Finance Enquiry'),
('Front Desk', 'Bus Service'),
('Front Desk', 'Appointment'),
('Front Desk', 'Job Interview'),
('Front Desk', 'Business Meeting');

-- --------------------------------------------------------

--
-- Table structure for table `total_queue`
--

CREATE TABLE `total_queue` (
  `Number` int(10) NOT NULL,
  `User_type` varchar(20) NOT NULL,
  `Request_type` varchar(50) NOT NULL,
  `Parent_name` varchar(40) NOT NULL,
  `Contact` varchar(20) NOT NULL,
  `Student_name` varchar(40) NOT NULL,
  `Student_id` varchar(11) NOT NULL,
  `Status` varchar(30) NOT NULL DEFAULT 'Waiting',
  `Total_time` time NOT NULL DEFAULT '00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `total_queue`
--

INSERT INTO `total_queue` (`Number`, `User_type`, `Request_type`, `Parent_name`, `Contact`, `Student_name`, `Student_id`, `Status`, `Total_time`) VALUES
(1, 'Parent', 'Academic Enquiry', 'Test1', '', 'Vuottek ', '3484', 'Completed', '00:01:20'),
(4, 'Parent', 'Bus Service', 'Test3', '', 'Vuottek Un', '3484', 'Completed', '01:28:02'),
(5, 'Parent', 'Academic Enquiry', 'Vuottek Un', '', 'Vuottek Un', '3484', 'Completed', '00:00:00'),
(10, 'Student', 'Academic Enquiry', '', '', '', '', 'Completed', '00:00:00'),
(11, 'Student', 'Transcript/Report Card', '', '', '', '', 'Completed', '00:00:00'),
(12, 'Parent', 'Transcript/Report Card', 'Test1', '', 'Vuottek Un', '3484', 'Completed', '00:00:00'),
(13, 'Parent', '', 'Vuottek Un', '', 'Vuottek Un', '3484', 'Waiting', '00:00:00'),
(14, 'Parent', '', 'Test1', '', 'Vuottek Un', '3484', 'Waiting', '00:00:00'),
(15, 'Parent', '', 'sada', '', 'asdas', 'asdas', 'Waiting', '00:00:00'),
(16, 'Parent', 'Academic Paperwork', 'Name', '', 'Vuottek ', '3484', 'Completed', '00:00:00'),
(17, 'Parent', '', 'Test2', '', 'Vuottek Un', '3484', 'Waiting', '00:00:00'),
(18, 'Visitor', '', 'James Bond', 'potatoe phone', '', '', 'Waiting', '00:00:00'),
(19, 'Student', 'Tuition Fee', '', '', 'James Bond', 'potatoe pho', 'In Progress', '00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `variables`
--

CREATE TABLE `variables` (
  `NUMBER` int(10) NOT NULL,
  `DEPARTMENT` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `variables`
--

INSERT INTO `variables` (`NUMBER`, `DEPARTMENT`) VALUES
(2, 'Accounting');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_queue`
--
ALTER TABLE `academic_queue`
  ADD PRIMARY KEY (`Number`) USING BTREE;

--
-- Indexes for table `accounting_queue`
--
ALTER TABLE `accounting_queue`
  ADD PRIMARY KEY (`Number`) USING BTREE;

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `front_desk_queue`
--
ALTER TABLE `front_desk_queue`
  ADD PRIMARY KEY (`Number`) USING BTREE;

--
-- Indexes for table `total_queue`
--
ALTER TABLE `total_queue`
  ADD PRIMARY KEY (`Number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `academic_queue`
--
ALTER TABLE `academic_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `accounting_queue`
--
ALTER TABLE `accounting_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `front_desk_queue`
--
ALTER TABLE `front_desk_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT for table `total_queue`
--
ALTER TABLE `total_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
