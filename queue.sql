-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 20, 2018 at 04:12 AM
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
-- Table structure for table `queue`
--

CREATE TABLE `queue` (
  `Number` int(10) NOT NULL,
  `User_type` varchar(20) NOT NULL,
  `Request` varchar(50) NOT NULL,
  `Parent_name` varchar(40) NOT NULL,
  `Contact` varchar(20) NOT NULL,
  `Student_name` varchar(40) NOT NULL,
  `Student_id` varchar(11) NOT NULL,
  `Status` varchar(30) NOT NULL,
  `Time_in` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Time_out` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `queue`
--

INSERT INTO `queue` (`Number`, `User_type`, `Request`, `Parent_name`, `Contact`, `Student_name`, `Student_id`, `Status`, `Time_in`, `Time_out`) VALUES
(1, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:21', '0000-00-00 00:00:00'),
(2, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:22', '0000-00-00 00:00:00'),
(3, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:23', '0000-00-00 00:00:00'),
(4, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:23', '0000-00-00 00:00:00'),
(5, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:24', '0000-00-00 00:00:00'),
(6, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:24', '0000-00-00 00:00:00'),
(7, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:25', '0000-00-00 00:00:00'),
(8, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:25', '0000-00-00 00:00:00'),
(9, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:26', '0000-00-00 00:00:00'),
(10, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:26', '0000-00-00 00:00:00'),
(11, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:27', '0000-00-00 00:00:00'),
(12, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:27', '0000-00-00 00:00:00'),
(13, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:27', '0000-00-00 00:00:00'),
(14, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:28', '0000-00-00 00:00:00'),
(15, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:45', '0000-00-00 00:00:00'),
(16, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:45', '0000-00-00 00:00:00'),
(17, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:46', '0000-00-00 00:00:00'),
(18, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:46', '0000-00-00 00:00:00'),
(19, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:46', '0000-00-00 00:00:00'),
(20, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:47', '0000-00-00 00:00:00'),
(21, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:47', '0000-00-00 00:00:00'),
(22, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:48', '0000-00-00 00:00:00'),
(23, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:48', '0000-00-00 00:00:00'),
(24, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:49', '0000-00-00 00:00:00'),
(25, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:49', '0000-00-00 00:00:00'),
(26, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:50', '0000-00-00 00:00:00'),
(27, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:50', '0000-00-00 00:00:00'),
(28, 'Parent', '', 'Un Pedech', '012404279', 'Vuottek Un', '3484', '', '2018-07-20 04:02:50', '0000-00-00 00:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `queue`
--
ALTER TABLE `queue`
  ADD KEY `Number` (`Number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `queue`
--
ALTER TABLE `queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
