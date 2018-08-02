-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 02, 2018 at 03:09 AM
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

-- --------------------------------------------------------

--
-- Table structure for table `variables`
--

CREATE TABLE `variables` (
  `NUMBER` int(10) NOT NULL,
  `DEPARTMENT` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

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
-- AUTO_INCREMENT for table `accounting_queue`
--
ALTER TABLE `accounting_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
--
-- AUTO_INCREMENT for table `front_desk_queue`
--
ALTER TABLE `front_desk_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT for table `total_queue`
--
ALTER TABLE `total_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
