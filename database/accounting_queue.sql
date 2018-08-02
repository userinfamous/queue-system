-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 02, 2018 at 03:59 AM
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

--
-- Dumping data for table `accounting_queue`
--

INSERT INTO `accounting_queue` (`Number`, `Time_in`, `Time_out`, `Time_diff`) VALUES
(1, '2018-08-01 08:00:40', '2018-08-01 08:15:14', '00:00:00'),
(2, '2018-08-01 08:18:48', '2018-08-01 08:19:19', '00:00:00'),
(3, '2018-08-01 09:41:30', '2018-08-01 09:41:41', '00:00:11'),
(4, '2018-08-01 09:51:48', '2018-08-01 09:51:58', '00:00:10'),
(5, '2018-08-01 10:00:24', '2018-08-01 10:01:20', '00:00:00'),
(6, '2018-08-01 10:02:18', '2018-08-01 10:02:30', '00:00:12'),
(7, '2018-08-01 10:05:33', '2018-08-01 10:05:43', '00:00:10'),
(8, '2018-08-01 10:36:47', '2018-08-01 10:37:15', '00:00:00'),
(9, '2018-08-01 10:37:44', '2018-08-01 10:37:51', '00:00:07'),
(10, '2018-08-01 10:39:58', '2018-08-01 10:54:47', '00:00:00'),
(11, '2018-08-01 10:55:26', '2018-08-01 10:55:33', '00:00:07'),
(12, '2018-08-01 10:56:43', '2018-08-01 10:56:51', '00:00:08'),
(13, '2018-08-01 13:40:20', '2018-08-01 13:40:23', '00:00:00'),
(14, '2018-08-02 02:29:42', '2018-08-02 02:30:16', '00:00:00'),
(15, '2018-08-02 02:31:33', '2018-08-02 02:31:45', '00:00:00'),
(16, '2018-08-02 03:05:10', '2018-08-02 03:05:24', '00:00:14');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounting_queue`
--
ALTER TABLE `accounting_queue`
  ADD PRIMARY KEY (`Number`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounting_queue`
--
ALTER TABLE `accounting_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
