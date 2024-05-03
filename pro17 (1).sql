-- phpMyAdmin SQL Dump
-- version 6.0.0-dev+20230302.b5e5e07f9a
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 02, 2024 at 06:13 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pro17`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `a_id` int(11) NOT NULL,
  `a_username` varchar(256) NOT NULL,
  `a_password` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`a_id`, `a_username`, `a_password`) VALUES
(2, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `ap_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `u_id` int(11) NOT NULL,
  `ap_time` varchar(256) NOT NULL,
  `ap_date` varchar(256) NOT NULL,
  `ap_report` varchar(256) NOT NULL,
  `ap_payment_status` enum('pending','success','failure') NOT NULL DEFAULT 'pending',
  `ap_status` enum('pending','accept','reject') NOT NULL DEFAULT 'pending',
  `razorpay_order_id` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`ap_id`, `d_id`, `u_id`, `ap_time`, `ap_date`, `ap_report`, `ap_payment_status`, `ap_status`, `razorpay_order_id`) VALUES
(15, 1, 5, '23:26', '2024-03-08', '31.jpg', 'success', 'accept', 'order_NjMDwMP1FHBJJf'),
(16, 1, 5, '04:02', '2024-03-09', 'pexels-eberhard-grossgasteiger-1612351.jpg', 'success', 'reject', 'order_NjNqHTPVh6O9K2'),
(17, 1, 5, '19:34', '2024-03-09', 'comparing-telegram-bot-hosting-providerspng.png', 'pending', 'pending', 'order_NkHbWUDZBVnK6p'),
(18, 1, 5, '22:26', '2024-03-10', 'WhatsApp Image 2024-01-18 at 13.01.39_ea96ab19.jpg', 'success', 'accept', 'order_NkKWxQrwzaEhGt');

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `d_id` int(11) NOT NULL,
  `d_name` varchar(256) NOT NULL,
  `d_email` varchar(256) NOT NULL,
  `d_passwords` varchar(256) NOT NULL,
  `d_spec` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`d_id`, `d_name`, `d_email`, `d_passwords`, `d_spec`) VALUES
(1, 'Dev', 'dev@gmail.com', 'Dev@1978', 'Rheumatologist'),
(8, 'rudra ', 'rudra1@gmail.com', 'dafa', 'Gastroenterologist'),
(9, 'Dinesh', 'dinesh@gmail.com', 'Dinesh@1978', 'Cardiologist'),
(10, 'Mayan', 'mayan@gmail.com', 'Mayan@1978', 'ENT specialist'),
(11, 'Paresh', 'paresh@gmail.com', 'Paresh@1978', 'Neurologist'),
(12, 'Urmik', 'urmik@gmail.com', 'Urmik@1978', 'Allergist'),
(13, 'Amit', 'Amit@gmail.com', 'Amit@1978', 'Urologist'),
(14, 'Rushi', 'Rushi@gmail.com', 'Rushi@1978', 'Dermatologist');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `u_id` int(11) NOT NULL,
  `u_name` varchar(256) NOT NULL,
  `u_email` varchar(256) NOT NULL,
  `u_password` varchar(256) NOT NULL,
  `u_mobile` bigint(20) NOT NULL,
  `u_age` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`u_id`, `u_name`, `u_email`, `u_password`, `u_mobile`, `u_age`) VALUES
(5, 'Rushi Gokani', 'rushigokani124@gmail.com', 'Rushi@1978', 7016031546, 25);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`a_id`);

--
-- Indexes for table `appointment`
--
ALTER TABLE `appointment`
  ADD PRIMARY KEY (`ap_id`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`d_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`u_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `a_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `appointment`
--
ALTER TABLE `appointment`
  MODIFY `ap_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `d_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `u_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
