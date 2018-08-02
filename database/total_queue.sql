-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 02, 2018 at 04:01 AM
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
(1, 'Visitor', 'Tuition Fee', 'sdasda', 'asdasd', 'sdasd', '', 'Completed', '00:00:07'),
(2, 'Visitor', 'Tuition Fee', 'asdasd', 'asdasd', 'asdaa', '', 'Completed', '00:00:07'),
(3, 'Visitor', 'Tuition Fee', 'asfa', 'asg', 'agas', '', 'Completed', '00:00:07'),
(4, 'Visitor', 'Tuition Fee', 'asdag', 'asfa', 'sdgd', '', 'Completed', '00:00:07'),
(5, 'Visitor', 'Tuition Fee', 'dga', 'ags', 'agsag', '', 'Completed', '00:00:07'),
(6, 'Visitor', 'Tuition Fee', 'asg', 'sgd', 'sgG', '', 'Completed', '00:00:07'),
(7, 'Visitor', 'Tuition Fee', 'AF', 'asg', 'adsg', '', 'Completed', '00:00:07'),
(8, 'Visitor', 'Tuition Fee', 'gdga', 'asga', 'sadgagfh', '', 'Completed', '00:00:07'),
(9, 'Visitor', 'Tuition Fee', 'asfa', 'fasf', 'asfa', '', 'Completed', '00:00:07'),
(10, 'Visitor', 'Tuition Fee', 'awg', 'awgag', 'wgawg', '', 'Completed', '00:00:07'),
(11, 'Visitor', 'Tuition Fee', 'asga', 'asgag', 'ggasga', '', 'Completed', '00:00:07'),
(12, 'Visitor', 'Tuition Fee', 'wadwaf', 'wafwaf', 'awfawf', '', 'Completed', '00:00:08'),
(13, 'Visitor', 'Information', 'sadasd', 'adsdas', 'asdasd', '', 'Completed', '00:00:00'),
(14, 'Visitor', 'Information', 'wadwqeq', 'qweqweq', 'eqweqwe', '', 'Completed', '00:00:15'),
(15, 'Visitor', 'Information', 'Test21', '081244888', 'Vuottek Un', '', 'Completed', '00:00:09'),
(16, 'Visitor', 'Information', 'Test2', 'adad', 'Hello', '', 'Completed', '00:00:22');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `total_queue`
--
ALTER TABLE `total_queue`
  ADD PRIMARY KEY (`Number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `total_queue`
--
ALTER TABLE `total_queue`
  MODIFY `Number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
