-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 28, 2018 at 04:28 PM
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
-- Table structure for table `check_changes`
--

CREATE TABLE `check_changes` (
  `id` int(11) NOT NULL,
  `recent_counter` varchar(10) NOT NULL,
  `old_counter` varchar(10) NOT NULL,
  `recent_display` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `check_changes`
--

INSERT INTO `check_changes` (`id`, `recent_counter`, `old_counter`, `recent_display`) VALUES
(0, '30', '30', 'False');

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
  `Counter_number` varchar(2) NOT NULL,
  `Total_time` time NOT NULL DEFAULT '00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
-- Indexes for table `check_changes`
--
ALTER TABLE `check_changes`
  ADD UNIQUE KEY `id` (`id`);

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
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `accounting_queue`
--
ALTER TABLE `accounting_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `front_desk_queue`
--
ALTER TABLE `front_desk_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `total_queue`
--
ALTER TABLE `total_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
