-- CREATE TABLE FOR USERS
-- CREATE TABLE users (
-- 	id SERIAL PRIMARY KEY,
-- 	matric_no VARCHAR(11) UNIQUE NOT NULL,
--     level INT NOT NULL,
--     surname VARCHAR(50) NOT NULL
-- );

-- TABLE FOR STUDENTS' DETAILS
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    level INT NOT NULL,
    matric_no VARCHAR(20) NOT NULL,
    department VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    pin VARCHAR(4) NOT NULL
);

-- TABLE FOR CANDIDATES' DETAILS
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    level INT NOT NULL,
    votes_count INT DEFAULT 0
);

-- TABLE FOR VOTES
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    voter INT NOT NULL REFERENCES students(id),
    candidate_id INT NOT NULL REFERENCES candidates(id)
);