-- Active: 1677500785362@@127.0.0.1@3306@boatdb

# Working on writing cleaner MySQL queries and better comments
# Initializing the Database
CREATE DATABASE exam_webapp;

# Selecting the new database
USE exam_webapp;


# Creating the table for teachers
CREATE TABLE teacher (
    teacher_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(100) NOT NULL
);

# Creating the table for students
CREATE TABLE student (
    student_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(100) NOT NULL
);

# Creating the table for the exams
CREATE TABLE exam (
    exam_id int NOT NULL AUTO_INCREMENT,
    teacher_id int,
    question1 varchar(255) NOT NULL,
    question2 varchar(255) NOT NULL,
    question3 varchar(255) NOT NULL,
    question4 varchar(255) NOT NULL,
    PRIMARY KEY (exam_id),
    FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id)
);

# Creating a table for completed exams
CREATE TABLE complete_exam (
    complete_exam_id int NOT NULL AUTO_INCREMENT,
    teacher_id int,
    exam_name varchar(100) NOT NULL,
    question1 varchar(255) NOT NULL,
    question2 varchar(255) NOT NULL,
    question3 varchar(255) NOT NULL,
    question4 varchar(255) NOT NULL,
    PRIMARY KEY (complete_exam_id),
    FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id)
);
