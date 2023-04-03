# Working on writing cleaner MySQL queries and better comments
# Initializing the Database
CREATE DATABASE testing_webapp;

# Selecting the new database
USE testing_webapp;

# Creating the table for all users
CREATE TABLE user (
    user_id int NOT NULL AUTO_INCREMENT,
    # Adding unique constraint to ensure there are no duplicate usernames
    username varchar(30) NOT NULL UNIQUE,
    name varchar(100) NOT NULL,
    password varchar(60) NOT NULL,
    user_type varchar(10) NOT NULL,
    PRIMARY KEY (user_id),
    # Adding a check to ensure the value given to user_type is either student or teacher
    CONSTRAINT user_type_check CHECK (LOWER(user_type) = 'student' OR LOWER(user_type) = 'teacher')
);

# Creating the table for teachers
CREATE TABLE teacher (
    teacher_id int NOT NULL AUTO_INCREMENT,
    user_id int,
    PRIMARY KEY (teacher_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

# Creating the table for students
CREATE TABLE student (
    student_id int NOT NULL AUTO_INCREMENT,
    user_id int,
    PRIMARY KEY (student_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

# Creating the table for the tests
CREATE TABLE test (
    test_id int NOT NULL AUTO_INCREMENT,
    teacher_id int,
    PRIMARY KEY (test_id),
    FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id)
);

# Creating a table for completed tests
CREATE TABLE complete_test (
    complete_test_id int NOT NULL AUTO_INCREMENT,
    student_id int,
    test_id int,
    PRIMARY KEY (complete_test_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (test_id) REFERENCES test(test_id)
);

# Creating the table for individual questions
CREATE TABLE question (
    question_id int NOT NULL AUTO_INCREMENT,
    test_id int,
    prompt varchar(2000) NOT NULL,
    PRIMARY KEY (question_id),
    FOREIGN KEY (test_id) REFERENCES test(test_id)
);

# Creating the table for the unique student answers
CREATE TABLE answer (
    question_id int,
    complete_test_id int,
    response varchar(3000) NOT NULL,
    # Using two foreign keys to create a compound primary key
    # This helps with enforcing unique values
    PRIMARY KEY (question_id, complete_test_id),
    FOREIGN KEY (question_id) REFERENCES question(question_id),
    FOREIGN KEY (complete_test_id) REFERENCES complete_test(complete_test_id)
);