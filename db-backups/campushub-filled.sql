--
-- PostgreSQL database dump
--

\restrict xkOe3JcnrFKTAOChvSqY9F5ql19kfVdcyCtbKfiFCH1mUorT9qB5XKrhRJVe1bt

-- Dumped from database version 18.1 (Debian 18.1-1.pgdg13+2)
-- Dumped by pg_dump version 18.1

-- Started on 2025-12-27 11:24:19 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 868 (class 1247 OID 16390)
-- Name: degree_level_enum; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.degree_level_enum AS ENUM (
    'Bachelor',
    'Master',
    'PhD'
);


ALTER TYPE public.degree_level_enum OWNER TO root;

--
-- TOC entry 877 (class 1247 OID 16450)
-- Name: employee_status_enum; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.employee_status_enum AS ENUM (
    'Active',
    'Inactive',
    'Suspended'
);


ALTER TYPE public.employee_status_enum OWNER TO root;

--
-- TOC entry 871 (class 1247 OID 16424)
-- Name: gender_enum; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.gender_enum AS ENUM (
    'Male',
    'Female',
    'Other'
);


ALTER TYPE public.gender_enum OWNER TO root;

--
-- TOC entry 880 (class 1247 OID 16458)
-- Name: student_status_enum; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.student_status_enum AS ENUM (
    'Active',
    'Inactive',
    'Suspended',
    'Graduated'
);


ALTER TYPE public.student_status_enum OWNER TO root;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 235 (class 1259 OID 16603)
-- Name: courses; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.courses (
    course_id integer NOT NULL,
    dept_id integer NOT NULL,
    course_code text NOT NULL,
    title text NOT NULL,
    description text,
    credits integer NOT NULL,
    CONSTRAINT courses_credits_check CHECK ((credits > 0))
);


ALTER TABLE public.courses OWNER TO root;

--
-- TOC entry 234 (class 1259 OID 16602)
-- Name: courses_course_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.courses_course_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.courses_course_id_seq OWNER TO root;

--
-- TOC entry 3565 (class 0 OID 0)
-- Dependencies: 234
-- Name: courses_course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.courses_course_id_seq OWNED BY public.courses.course_id;


--
-- TOC entry 230 (class 1259 OID 16548)
-- Name: department_heads; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.department_heads (
    dept_id integer NOT NULL,
    employee_id integer NOT NULL,
    start_date date NOT NULL,
    end_date date
);


ALTER TABLE public.department_heads OWNER TO root;

--
-- TOC entry 229 (class 1259 OID 16535)
-- Name: departments; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.departments (
    dept_id integer NOT NULL,
    name text NOT NULL,
    code text NOT NULL
);


ALTER TABLE public.departments OWNER TO root;

--
-- TOC entry 228 (class 1259 OID 16534)
-- Name: departments_dept_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.departments_dept_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.departments_dept_id_seq OWNER TO root;

--
-- TOC entry 3566 (class 0 OID 0)
-- Dependencies: 228
-- Name: departments_dept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.departments_dept_id_seq OWNED BY public.departments.dept_id;


--
-- TOC entry 227 (class 1259 OID 16516)
-- Name: employee_positions; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.employee_positions (
    employee_id integer NOT NULL,
    position_id integer NOT NULL,
    start_date date NOT NULL,
    end_date date
);


ALTER TABLE public.employee_positions OWNER TO root;

--
-- TOC entry 224 (class 1259 OID 16486)
-- Name: employees; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.employees (
    employee_id integer NOT NULL,
    person_id integer NOT NULL,
    employment_date date NOT NULL,
    status public.employee_status_enum NOT NULL
);


ALTER TABLE public.employees OWNER TO root;

--
-- TOC entry 223 (class 1259 OID 16485)
-- Name: employees_employee_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.employees_employee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_employee_id_seq OWNER TO root;

--
-- TOC entry 3567 (class 0 OID 0)
-- Dependencies: 223
-- Name: employees_employee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.employees_employee_id_seq OWNED BY public.employees.employee_id;


--
-- TOC entry 232 (class 1259 OID 16566)
-- Name: majors; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.majors (
    major_id integer NOT NULL,
    dept_id integer NOT NULL,
    name text NOT NULL,
    degree_level public.degree_level_enum NOT NULL
);


ALTER TABLE public.majors OWNER TO root;

--
-- TOC entry 231 (class 1259 OID 16565)
-- Name: majors_major_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.majors_major_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.majors_major_id_seq OWNER TO root;

--
-- TOC entry 3568 (class 0 OID 0)
-- Dependencies: 231
-- Name: majors_major_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.majors_major_id_seq OWNED BY public.majors.major_id;


--
-- TOC entry 220 (class 1259 OID 16432)
-- Name: persons; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.persons (
    person_id integer NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    date_of_birth date,
    pesel character varying(11) NOT NULL,
    gender public.gender_enum,
    email text NOT NULL,
    phone_number text,
    address text
);


ALTER TABLE public.persons OWNER TO root;

--
-- TOC entry 219 (class 1259 OID 16431)
-- Name: persons_person_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.persons_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.persons_person_id_seq OWNER TO root;

--
-- TOC entry 3569 (class 0 OID 0)
-- Dependencies: 219
-- Name: persons_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.persons_person_id_seq OWNED BY public.persons.person_id;


--
-- TOC entry 226 (class 1259 OID 16504)
-- Name: positions; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.positions (
    position_id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.positions OWNER TO root;

--
-- TOC entry 225 (class 1259 OID 16503)
-- Name: positions_position_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.positions_position_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.positions_position_id_seq OWNER TO root;

--
-- TOC entry 3570 (class 0 OID 0)
-- Dependencies: 225
-- Name: positions_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.positions_position_id_seq OWNED BY public.positions.position_id;


--
-- TOC entry 233 (class 1259 OID 16583)
-- Name: student_majors; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.student_majors (
    student_id integer NOT NULL,
    major_id integer NOT NULL,
    start_date date NOT NULL,
    end_date date,
    is_primary boolean DEFAULT false
);


ALTER TABLE public.student_majors OWNER TO root;

--
-- TOC entry 222 (class 1259 OID 16468)
-- Name: students; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.students (
    student_id integer NOT NULL,
    person_id integer NOT NULL,
    enrollment_date date NOT NULL,
    status public.student_status_enum NOT NULL
);


ALTER TABLE public.students OWNER TO root;

--
-- TOC entry 221 (class 1259 OID 16467)
-- Name: students_student_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.students_student_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.students_student_id_seq OWNER TO root;

--
-- TOC entry 3571 (class 0 OID 0)
-- Dependencies: 221
-- Name: students_student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.students_student_id_seq OWNED BY public.students.student_id;


--
-- TOC entry 3350 (class 2604 OID 16606)
-- Name: courses course_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.courses ALTER COLUMN course_id SET DEFAULT nextval('public.courses_course_id_seq'::regclass);


--
-- TOC entry 3347 (class 2604 OID 16538)
-- Name: departments dept_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.departments ALTER COLUMN dept_id SET DEFAULT nextval('public.departments_dept_id_seq'::regclass);


--
-- TOC entry 3345 (class 2604 OID 16489)
-- Name: employees employee_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employees ALTER COLUMN employee_id SET DEFAULT nextval('public.employees_employee_id_seq'::regclass);


--
-- TOC entry 3348 (class 2604 OID 16569)
-- Name: majors major_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.majors ALTER COLUMN major_id SET DEFAULT nextval('public.majors_major_id_seq'::regclass);


--
-- TOC entry 3343 (class 2604 OID 16435)
-- Name: persons person_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persons ALTER COLUMN person_id SET DEFAULT nextval('public.persons_person_id_seq'::regclass);


--
-- TOC entry 3346 (class 2604 OID 16507)
-- Name: positions position_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.positions ALTER COLUMN position_id SET DEFAULT nextval('public.positions_position_id_seq'::regclass);


--
-- TOC entry 3344 (class 2604 OID 16471)
-- Name: students student_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.students ALTER COLUMN student_id SET DEFAULT nextval('public.students_student_id_seq'::regclass);


--
-- TOC entry 3559 (class 0 OID 16603)
-- Dependencies: 235
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (1, 1, 'CS101', 'Intro to Programming', 'Basics of programming', 5);
INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (2, 1, 'CS201', 'Data Structures', 'Algorithms and data structures', 6);
INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (3, 2, 'MATH101', 'Calculus I', 'Differential calculus', 5);
INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (4, 3, 'PHYS101', 'Classical Mechanics', 'Newtonian mechanics', 5);
INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (5, 4, 'CHEM101', 'General Chemistry', 'Chemical principles', 5);
INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (6, 5, 'BIO201', 'Molecular Biology', 'DNA and proteins', 6);
INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (7, 6, 'ECON101', 'Microeconomics', 'Market behavior', 5);
INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (8, 7, 'HIST101', 'World History', 'Global history overview', 4);
INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (9, 8, 'PHIL201', 'Ethics', 'Moral philosophy', 4);
INSERT INTO public.courses (course_id, dept_id, course_code, title, description, credits) VALUES (10, 9, 'ME101', 'Statics', 'Engineering statics', 5);


--
-- TOC entry 3554 (class 0 OID 16548)
-- Dependencies: 230
-- Data for Name: department_heads; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (1, 1, '2020-01-01', NULL);
INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (2, 2, '2020-01-01', NULL);
INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (3, 3, '2020-01-01', NULL);
INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (4, 4, '2020-01-01', NULL);
INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (5, 5, '2020-01-01', NULL);
INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (6, 6, '2020-01-01', NULL);
INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (7, 7, '2020-01-01', NULL);
INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (8, 8, '2020-01-01', NULL);
INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (9, 9, '2020-01-01', NULL);
INSERT INTO public.department_heads (dept_id, employee_id, start_date, end_date) VALUES (10, 10, '2020-01-01', NULL);


--
-- TOC entry 3553 (class 0 OID 16535)
-- Dependencies: 229
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.departments (dept_id, name, code) VALUES (1, 'Computer Science', 'CS');
INSERT INTO public.departments (dept_id, name, code) VALUES (2, 'Mathematics', 'MATH');
INSERT INTO public.departments (dept_id, name, code) VALUES (3, 'Physics', 'PHYS');
INSERT INTO public.departments (dept_id, name, code) VALUES (4, 'Chemistry', 'CHEM');
INSERT INTO public.departments (dept_id, name, code) VALUES (5, 'Biology', 'BIO');
INSERT INTO public.departments (dept_id, name, code) VALUES (6, 'Economics', 'ECON');
INSERT INTO public.departments (dept_id, name, code) VALUES (7, 'History', 'HIST');
INSERT INTO public.departments (dept_id, name, code) VALUES (8, 'Philosophy', 'PHIL');
INSERT INTO public.departments (dept_id, name, code) VALUES (9, 'Mechanical Engineering', 'ME');
INSERT INTO public.departments (dept_id, name, code) VALUES (10, 'Electrical Engineering', 'EE');


--
-- TOC entry 3551 (class 0 OID 16516)
-- Dependencies: 227
-- Data for Name: employee_positions; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (1, 1, '2005-10-01', NULL);
INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (2, 2, '2008-10-01', NULL);
INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (3, 3, '2010-10-01', NULL);
INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (4, 4, '2015-10-01', NULL);
INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (5, 1, '2007-10-01', NULL);
INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (6, 5, '2012-10-01', NULL);
INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (7, 10, '2018-10-01', NULL);
INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (8, 8, '2019-10-01', NULL);
INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (9, 9, '2020-10-01', NULL);
INSERT INTO public.employee_positions (employee_id, position_id, start_date, end_date) VALUES (10, 6, '2016-10-01', NULL);


--
-- TOC entry 3548 (class 0 OID 16486)
-- Dependencies: 224
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (1, 1, '2005-10-01', 'Active');
INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (2, 2, '2008-10-01', 'Active');
INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (3, 3, '2010-10-01', 'Active');
INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (4, 4, '2015-10-01', 'Active');
INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (5, 5, '2007-10-01', 'Active');
INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (6, 6, '2012-10-01', 'Active');
INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (7, 7, '2018-10-01', 'Active');
INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (8, 8, '2019-10-01', 'Active');
INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (9, 9, '2020-10-01', 'Active');
INSERT INTO public.employees (employee_id, person_id, employment_date, status) VALUES (10, 10, '2016-10-01', 'Active');


--
-- TOC entry 3556 (class 0 OID 16566)
-- Dependencies: 232
-- Data for Name: majors; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (1, 1, 'Computer Science', 'Bachelor');
INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (2, 1, 'Computer Science', 'Master');
INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (3, 2, 'Applied Mathematics', 'Bachelor');
INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (4, 3, 'Physics', 'Bachelor');
INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (5, 4, 'Chemistry', 'Bachelor');
INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (6, 5, 'Biotechnology', 'Master');
INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (7, 6, 'Economics', 'Bachelor');
INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (8, 7, 'History', 'Bachelor');
INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (9, 8, 'Philosophy', 'Master');
INSERT INTO public.majors (major_id, dept_id, name, degree_level) VALUES (10, 9, 'Mechanical Engineering', 'Bachelor');


--
-- TOC entry 3544 (class 0 OID 16432)
-- Dependencies: 220
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (1, 'Adam', 'Kowalski', '1975-03-12', '75031200001', 'Male', 'adam.kowalski@uni.edu', '500100001', 'Krakow');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (2, 'Anna', 'Nowak', '1980-07-22', '80072200002', 'Female', 'anna.nowak@uni.edu', '500100002', 'Warsaw');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (3, 'Piotr', 'Zielinski', '1985-11-02', '85110200003', 'Male', 'piotr.zielinski@uni.edu', '500100003', 'Gdansk');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (4, 'Maria', 'Wisniewska', '1990-01-18', '90011800004', 'Female', 'maria.w@uni.edu', '500100004', 'Poznan');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (5, 'Tomasz', 'Wojcik', '1978-05-30', '78053000005', 'Male', 'tomasz.wojcik@uni.edu', '500100005', 'Wroclaw');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (6, 'Katarzyna', 'Lewandowska', '1983-09-14', '83091400006', 'Female', 'k.lewandowska@uni.edu', '500100006', 'Lodz');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (7, 'Michal', 'Kaminski', '1992-02-09', '92020900007', 'Male', 'm.kaminski@uni.edu', '500100007', 'Krakow');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (8, 'Agnieszka', 'Dabrowska', '1994-06-21', '94062100008', 'Female', 'a.dabrowska@uni.edu', '500100008', 'Szczecin');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (9, 'Pawel', 'Kaczmarek', '1996-10-11', '96101100009', 'Male', 'pawel.k@uni.edu', '500100009', 'Katowice');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (10, 'Natalia', 'Piotrowska', '1997-12-05', '97120500010', 'Female', 'n.piotrowska@uni.edu', '500100010', 'Lublin');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (11, 'Jan', 'Mazur', '2000-03-03', '00030300011', 'Male', 'jan.mazur@student.edu', '500200011', 'Krakow');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (12, 'Julia', 'Krol', '2001-07-07', '01070700012', 'Female', 'julia.krol@student.edu', '500200012', 'Warsaw');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (13, 'Oskar', 'Wieczorek', '1999-09-09', '99090900013', 'Male', 'oskar.w@student.edu', '500200013', 'Gdansk');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (14, 'Zuzanna', 'Jablonska', '2002-01-15', '02011500014', 'Female', 'z.jablonska@student.edu', '500200014', 'Poznan');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (15, 'Filip', 'Pawlowski', '2001-11-23', '01112300015', 'Male', 'filip.p@student.edu', '500200015', 'Wroclaw');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (16, 'Maja', 'Sikora', '2000-04-19', '00041900016', 'Female', 'maja.s@student.edu', '500200016', 'Lodz');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (17, 'Kacper', 'Chmielewski', '1998-06-30', '98063000017', 'Male', 'k.chmielewski@student.edu', '500200017', 'Krakow');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (18, 'Alicja', 'Czarnecka', '1999-08-08', '99080800018', 'Female', 'alicja.c@student.edu', '500200018', 'Rzeszow');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (19, 'Hubert', 'Borkowski', '2002-02-02', '02020200019', 'Male', 'hubert.b@student.edu', '500200019', 'Opole');
INSERT INTO public.persons (person_id, first_name, last_name, date_of_birth, pesel, gender, email, phone_number, address) VALUES (20, 'Laura', 'Sawicka', '2001-12-12', '01121200020', 'Female', 'laura.s@student.edu', '500200020', 'Olsztyn');


--
-- TOC entry 3550 (class 0 OID 16504)
-- Dependencies: 226
-- Data for Name: positions; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.positions (position_id, name) VALUES (1, 'Professor');
INSERT INTO public.positions (position_id, name) VALUES (2, 'Associate Professor');
INSERT INTO public.positions (position_id, name) VALUES (3, 'Assistant Professor');
INSERT INTO public.positions (position_id, name) VALUES (4, 'Lecturer');
INSERT INTO public.positions (position_id, name) VALUES (5, 'Researcher');
INSERT INTO public.positions (position_id, name) VALUES (6, 'Department Secretary');
INSERT INTO public.positions (position_id, name) VALUES (7, 'Dean');
INSERT INTO public.positions (position_id, name) VALUES (8, 'Lab Technician');
INSERT INTO public.positions (position_id, name) VALUES (9, 'Administrator');
INSERT INTO public.positions (position_id, name) VALUES (10, 'Teaching Assistant');


--
-- TOC entry 3557 (class 0 OID 16583)
-- Dependencies: 233
-- Data for Name: student_majors; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (1, 1, '2019-10-01', NULL, true);
INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (2, 2, '2019-10-01', NULL, true);
INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (3, 3, '2018-10-01', NULL, true);
INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (4, 4, '2020-10-01', NULL, true);
INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (5, 5, '2019-10-01', NULL, true);
INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (6, 6, '2018-10-01', NULL, true);
INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (7, 7, '2017-10-01', NULL, true);
INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (8, 8, '2019-10-01', NULL, true);
INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (9, 9, '2020-10-01', NULL, true);
INSERT INTO public.student_majors (student_id, major_id, start_date, end_date, is_primary) VALUES (10, 10, '2019-10-01', NULL, true);


--
-- TOC entry 3546 (class 0 OID 16468)
-- Dependencies: 222
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (1, 11, '2019-10-01', 'Active');
INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (2, 12, '2019-10-01', 'Active');
INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (3, 13, '2018-10-01', 'Graduated');
INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (4, 14, '2020-10-01', 'Active');
INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (5, 15, '2019-10-01', 'Active');
INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (6, 16, '2018-10-01', 'Graduated');
INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (7, 17, '2017-10-01', 'Graduated');
INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (8, 18, '2019-10-01', 'Active');
INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (9, 19, '2020-10-01', 'Active');
INSERT INTO public.students (student_id, person_id, enrollment_date, status) VALUES (10, 20, '2019-10-01', 'Active');


--
-- TOC entry 3572 (class 0 OID 0)
-- Dependencies: 234
-- Name: courses_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.courses_course_id_seq', 10, true);


--
-- TOC entry 3573 (class 0 OID 0)
-- Dependencies: 228
-- Name: departments_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.departments_dept_id_seq', 10, true);


--
-- TOC entry 3574 (class 0 OID 0)
-- Dependencies: 223
-- Name: employees_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.employees_employee_id_seq', 10, true);


--
-- TOC entry 3575 (class 0 OID 0)
-- Dependencies: 231
-- Name: majors_major_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.majors_major_id_seq', 10, true);


--
-- TOC entry 3576 (class 0 OID 0)
-- Dependencies: 219
-- Name: persons_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.persons_person_id_seq', 20, true);


--
-- TOC entry 3577 (class 0 OID 0)
-- Dependencies: 225
-- Name: positions_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.positions_position_id_seq', 10, true);


--
-- TOC entry 3578 (class 0 OID 0)
-- Dependencies: 221
-- Name: students_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.students_student_id_seq', 10, true);


--
-- TOC entry 3382 (class 2606 OID 16618)
-- Name: courses courses_course_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_course_code_key UNIQUE (course_code);


--
-- TOC entry 3384 (class 2606 OID 16616)
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (course_id);


--
-- TOC entry 3373 (class 2606 OID 16547)
-- Name: departments departments_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_code_key UNIQUE (code);


--
-- TOC entry 3375 (class 2606 OID 16545)
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (dept_id);


--
-- TOC entry 3371 (class 2606 OID 16523)
-- Name: employee_positions employee_positions_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employee_positions
    ADD CONSTRAINT employee_positions_pkey PRIMARY KEY (employee_id, position_id, start_date);


--
-- TOC entry 3363 (class 2606 OID 16497)
-- Name: employees employees_person_id_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_person_id_key UNIQUE (person_id);


--
-- TOC entry 3365 (class 2606 OID 16495)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (employee_id);


--
-- TOC entry 3378 (class 2606 OID 16577)
-- Name: majors majors_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.majors
    ADD CONSTRAINT majors_pkey PRIMARY KEY (major_id);


--
-- TOC entry 3353 (class 2606 OID 16448)
-- Name: persons persons_email_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_email_key UNIQUE (email);


--
-- TOC entry 3355 (class 2606 OID 16446)
-- Name: persons persons_pesel_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pesel_key UNIQUE (pesel);


--
-- TOC entry 3357 (class 2606 OID 16444)
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (person_id);


--
-- TOC entry 3367 (class 2606 OID 16515)
-- Name: positions positions_name_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_name_key UNIQUE (name);


--
-- TOC entry 3369 (class 2606 OID 16513)
-- Name: positions positions_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_pkey PRIMARY KEY (position_id);


--
-- TOC entry 3380 (class 2606 OID 16591)
-- Name: student_majors student_majors_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.student_majors
    ADD CONSTRAINT student_majors_pkey PRIMARY KEY (student_id, major_id, start_date);


--
-- TOC entry 3359 (class 2606 OID 16479)
-- Name: students students_person_id_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_person_id_key UNIQUE (person_id);


--
-- TOC entry 3361 (class 2606 OID 16477)
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (student_id);


--
-- TOC entry 3385 (class 1259 OID 16624)
-- Name: idx_courses_course_code; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX idx_courses_course_code ON public.courses USING btree (course_code);


--
-- TOC entry 3376 (class 1259 OID 16564)
-- Name: one_active_head_per_department; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX one_active_head_per_department ON public.department_heads USING btree (dept_id) WHERE (end_date IS NULL);


--
-- TOC entry 3395 (class 2606 OID 16619)
-- Name: courses fk_courses_department; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT fk_courses_department FOREIGN KEY (dept_id) REFERENCES public.departments(dept_id) ON DELETE CASCADE;


--
-- TOC entry 3390 (class 2606 OID 16554)
-- Name: department_heads fk_dh_department; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.department_heads
    ADD CONSTRAINT fk_dh_department FOREIGN KEY (dept_id) REFERENCES public.departments(dept_id) ON DELETE CASCADE;


--
-- TOC entry 3391 (class 2606 OID 16559)
-- Name: department_heads fk_dh_employee; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.department_heads
    ADD CONSTRAINT fk_dh_employee FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id);


--
-- TOC entry 3387 (class 2606 OID 16498)
-- Name: employees fk_employees_person; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT fk_employees_person FOREIGN KEY (person_id) REFERENCES public.persons(person_id) ON DELETE CASCADE;


--
-- TOC entry 3388 (class 2606 OID 16524)
-- Name: employee_positions fk_ep_employee; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employee_positions
    ADD CONSTRAINT fk_ep_employee FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id) ON DELETE CASCADE;


--
-- TOC entry 3389 (class 2606 OID 16529)
-- Name: employee_positions fk_ep_position; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employee_positions
    ADD CONSTRAINT fk_ep_position FOREIGN KEY (position_id) REFERENCES public.positions(position_id);


--
-- TOC entry 3392 (class 2606 OID 16578)
-- Name: majors fk_majors_department; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.majors
    ADD CONSTRAINT fk_majors_department FOREIGN KEY (dept_id) REFERENCES public.departments(dept_id) ON DELETE CASCADE;


--
-- TOC entry 3393 (class 2606 OID 16597)
-- Name: student_majors fk_sm_major; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.student_majors
    ADD CONSTRAINT fk_sm_major FOREIGN KEY (major_id) REFERENCES public.majors(major_id) ON DELETE CASCADE;


--
-- TOC entry 3394 (class 2606 OID 16592)
-- Name: student_majors fk_sm_student; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.student_majors
    ADD CONSTRAINT fk_sm_student FOREIGN KEY (student_id) REFERENCES public.students(student_id) ON DELETE CASCADE;


--
-- TOC entry 3386 (class 2606 OID 16480)
-- Name: students fk_students_person; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT fk_students_person FOREIGN KEY (person_id) REFERENCES public.persons(person_id) ON DELETE CASCADE;


-- Completed on 2025-12-27 11:24:19 UTC

--
-- PostgreSQL database dump complete
--

\unrestrict xkOe3JcnrFKTAOChvSqY9F5ql19kfVdcyCtbKfiFCH1mUorT9qB5XKrhRJVe1bt

