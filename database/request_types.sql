-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 08, 2018 at 07:44 AM
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
('Accounting', 'Accessory Fee'),
('Accounting', 'Payment'),
('Front Desk', 'Late Slip'),
('Front Desk', 'Reenrollment'),
('Front Desk', 'Lost and Found'),
('Academic', 'Academic Paperwork'),
('Academic', 'Enquiry'),
('Academic', 'Transcript/Report Card'),
('Accounting', 'Enquiry'),
('Front Desk', 'Bus Service'),
('Front Desk', 'Appointment'),
('Front Desk', 'Job Interview'),
('Front Desk', 'Business Meeting');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
