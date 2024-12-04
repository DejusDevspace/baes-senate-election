-- TABLE FOR STUDENTS' DETAILS
DROP TABLE IF EXISTS students CASCADE;
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    level INT NOT NULL,
    matric_no VARCHAR(20) NOT NULL,
    department VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    pin VARCHAR(4) NOT NULL
);

-- TABLE FOR CANDIDATES' DETAILS
DROP TABLE IF EXISTS candidates CASCADE;
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    level INT NOT NULL,
    department VARCHAR(50) NOT NULL,
    image VARCHAR(255) NOT NULL,
    votes_count INT DEFAULT 0
);

-- TABLE FOR VOTES
DROP TABLE IF EXISTS votes CASCADE;
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    voter INT NOT NULL REFERENCES students(id),
    candidate_id INT NOT NULL REFERENCES candidates(id)
);

-- Dummy data for db testing
INSERT INTO students (level, matric_no, surname, pin, department)
VALUES (500, 'BU20MCT1017', 'Adejo', 1234, 'Mechatronics Engineering'),
(400, 'BU20EEE1000', 'Doe', 2222, 'Electrical and Electronics Engineering'),
(300, 'BU20MCT1000', 'Doe', 3333, 'Mechatronics Engineering'),
(200, 'BU20EEE1001', 'Doe', 4444, 'Electrical and Electronics Engineering'),
(500, 'BU20EEE1002', 'Doe', 5555, 'Electrical and Electronics Engineering'),
(400, 'BU20MCT1002', 'Doe', 6666, 'Mechatronics Engineering'),
(300, 'BU20EEE1003', 'Doe', 7777, 'Electrical and Electronics Engineering');

INSERT INTO candidates (name, position, level, department, image)
VALUES
('John Doe', 'Chairman', 200, 'Electrical and Electronics Engineering', 'assets/img/candidates/image524.png'),
('Mary Doe', 'Head', 500, 'Mechatronics Engineering', 'assets/img/candidates/image526.png'),
('Jack Harry', 'Chairman', 500, 'Mechatronics Engineering', 'assets/img/candidates/image524.png'),
('Blake James', 'Chairman', 300, 'Mechatronics Engineering', 'assets/img/candidates/image525.png'),
('Invalid Dan', 'Chairman', 300, 'Electrical and Electronics Engineering', 'assets/img/candidates/image524.png'),
('Jane Glory', 'Chairman', 400, 'Electrical and Electronics Engineering', 'assets/img/candidates/image526.png'),
('Mark Doe', 'Head', 500, 'Electrical and Electronics Engineering', 'assets/img/candidates/image525.png'),
('Paul Doe', 'Chairman', 400, 'Mechatronics Engineering', 'assets/img/candidates/image524.png');
