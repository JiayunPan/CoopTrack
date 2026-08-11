-- Clean MySQL schema. Open this file in a NEW DataGrip editor tab.
CREATE DATABASE IF NOT EXISTS cooptrack;

USE cooptrack;

CREATE TABLE admin (
    admin_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE coordinator (
    coordinator_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE alum (
    alum_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    major VARCHAR(100)
);

CREATE TABLE recruiting_term (
    term_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    season VARCHAR(30) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CONSTRAINT recruiting_term_dates_check CHECK (end_date >= start_date)
);

CREATE TABLE student (
    student_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    major VARCHAR(100),
    active_status BOOLEAN NOT NULL DEFAULT TRUE,
    resume_url VARCHAR(500),
    suspended_by_admin_id BIGINT,
    CONSTRAINT student_suspended_by_admin_fk
        FOREIGN KEY (suspended_by_admin_id) REFERENCES admin (admin_id)
);

CREATE TABLE employer (
    employer_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    verification_status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    verified_by_admin_id BIGINT,
    CONSTRAINT employer_verified_by_admin_fk
        FOREIGN KEY (verified_by_admin_id) REFERENCES admin (admin_id)
);

CREATE TABLE skill (
    skill_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    skill_status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    managed_by_admin_id BIGINT,
    CONSTRAINT skill_managed_by_admin_fk
        FOREIGN KEY (managed_by_admin_id) REFERENCES admin (admin_id)
);

CREATE TABLE position (
    position_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    employer_id BIGINT NOT NULL,
    term_id BIGINT NOT NULL,
    moderated_by_admin_id BIGINT,
    position_title VARCHAR(150) NOT NULL,
    description TEXT,
    location VARCHAR(150),
    work_mode VARCHAR(30),
    employment_type VARCHAR(30),
    position_status VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    application_deadline DATE,
    CONSTRAINT position_employer_fk
        FOREIGN KEY (employer_id) REFERENCES employer (employer_id),
    CONSTRAINT position_term_fk
        FOREIGN KEY (term_id) REFERENCES recruiting_term (term_id),
    CONSTRAINT position_moderated_by_admin_fk
        FOREIGN KEY (moderated_by_admin_id) REFERENCES admin (admin_id)
);

CREATE TABLE application (
    application_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT NOT NULL,
    position_id BIGINT NOT NULL,
    submitted_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    application_status VARCHAR(30) NOT NULL DEFAULT 'SUBMITTED',
    interview_date TIMESTAMP,
    offer_date DATE,
    accepted_date DATE,
    CONSTRAINT application_student_fk
        FOREIGN KEY (student_id) REFERENCES student (student_id),
    CONSTRAINT application_position_fk
        FOREIGN KEY (position_id) REFERENCES position (position_id),
    CONSTRAINT application_student_position_unique
        UNIQUE (student_id, position_id)
);

CREATE TABLE student_skill (
    student_id BIGINT NOT NULL,
    skill_id BIGINT NOT NULL,
    PRIMARY KEY (student_id, skill_id),
    CONSTRAINT student_skill_student_fk
        FOREIGN KEY (student_id) REFERENCES student (student_id),
    CONSTRAINT student_skill_skill_fk
        FOREIGN KEY (skill_id) REFERENCES skill (skill_id)
);

CREATE TABLE position_skill (
    position_id BIGINT NOT NULL,
    skill_id BIGINT NOT NULL,
    PRIMARY KEY (position_id, skill_id),
    CONSTRAINT position_skill_position_fk
        FOREIGN KEY (position_id) REFERENCES position (position_id),
    CONSTRAINT position_skill_skill_fk
        FOREIGN KEY (skill_id) REFERENCES skill (skill_id)
);

CREATE TABLE saved_position (
    student_id BIGINT NOT NULL,
    position_id BIGINT NOT NULL,
    PRIMARY KEY (student_id, position_id),
    CONSTRAINT saved_position_student_fk
        FOREIGN KEY (student_id) REFERENCES student (student_id),
    CONSTRAINT saved_position_position_fk
        FOREIGN KEY (position_id) REFERENCES position (position_id)
);

CREATE TABLE report (
    report_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT NOT NULL,
    position_id BIGINT NOT NULL,
    reviewed_by_admin_id BIGINT,
    reason TEXT NOT NULL,
    reported_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    review_status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    CONSTRAINT report_student_fk
        FOREIGN KEY (student_id) REFERENCES student (student_id),
    CONSTRAINT report_position_fk
        FOREIGN KEY (position_id) REFERENCES position (position_id),
    CONSTRAINT report_reviewed_by_admin_fk
        FOREIGN KEY (reviewed_by_admin_id) REFERENCES admin (admin_id)
);

CREATE TABLE question (
    question_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT NOT NULL,
    answered_by_alum_id BIGINT,
    question_text TEXT NOT NULL,
    posted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    answer_text TEXT,
    answered_at TIMESTAMP,
    CONSTRAINT question_student_fk
        FOREIGN KEY (student_id) REFERENCES student (student_id),
    CONSTRAINT question_answered_by_alum_fk
        FOREIGN KEY (answered_by_alum_id) REFERENCES alum (alum_id)
);

CREATE TABLE review (
    review_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    alum_id BIGINT NOT NULL,
    employer_id BIGINT NOT NULL,
    rating INTEGER NOT NULL,
    review_text TEXT,
    posted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT review_alum_fk
        FOREIGN KEY (alum_id) REFERENCES alum (alum_id),
    CONSTRAINT review_employer_fk
        FOREIGN KEY (employer_id) REFERENCES employer (employer_id),
    CONSTRAINT review_rating_check CHECK (rating BETWEEN 1 AND 5)
);

CREATE TABLE experience (
    experience_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    alum_id BIGINT NOT NULL,
    employer_id BIGINT NOT NULL,
    role_title VARCHAR(150) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    CONSTRAINT experience_alum_fk
        FOREIGN KEY (alum_id) REFERENCES alum (alum_id),
    CONSTRAINT experience_employer_fk
        FOREIGN KEY (employer_id) REFERENCES employer (employer_id),
    CONSTRAINT experience_dates_check
        CHECK (end_date IS NULL OR end_date >= start_date)
);

CREATE TABLE alum_recommendation (
    alum_id BIGINT NOT NULL,
    position_id BIGINT NOT NULL,
    PRIMARY KEY (alum_id, position_id),
    CONSTRAINT alum_recommendation_alum_fk
        FOREIGN KEY (alum_id) REFERENCES alum (alum_id),
    CONSTRAINT alum_recommendation_position_fk
        FOREIGN KEY (position_id) REFERENCES position (position_id)
);

CREATE TABLE coordinator_term (
    coordinator_id BIGINT NOT NULL,
    term_id BIGINT NOT NULL,
    PRIMARY KEY (coordinator_id, term_id),
    CONSTRAINT coordinator_term_coordinator_fk
        FOREIGN KEY (coordinator_id) REFERENCES coordinator (coordinator_id),
    CONSTRAINT coordinator_term_term_fk
        FOREIGN KEY (term_id) REFERENCES recruiting_term (term_id)
);
