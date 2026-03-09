-- Create database for voting system
CREATE DATABASE IF NOT EXISTS voting_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Grant privileges to root user
GRANT ALL PRIVILEGES ON voting_system.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

-- Show databases to confirm
SHOW DATABASES;
