--
-- PostgreSQL database dump
--

\restrict meYmOz8vfKkVfbbOQDlMQ2CQeT7dGqUDyO4oyu87q4YPavejjCIUPwitCZoF2z9

-- Dumped from database version 18.1 (Debian 18.1-1.pgdg13+2)
-- Dumped by pg_dump version 18.1

-- Started on 2026-01-08 17:43:25 UTC

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
-- TOC entry 870 (class 1247 OID 16388)
-- Name: degree_level_enum; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.degree_level_enum AS ENUM (
    'Bachelor',
    'Master',
    'PhD'
);


ALTER TYPE public.degree_level_enum OWNER TO root;

--
-- TOC entry 873 (class 1247 OID 16396)
-- Name: employee_status_enum; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.employee_status_enum AS ENUM (
    'Active',
    'Inactive',
    'Suspended'
);


ALTER TYPE public.employee_status_enum OWNER TO root;

--
-- TOC entry 876 (class 1247 OID 16404)
-- Name: gender_enum; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.gender_enum AS ENUM (
    'Male',
    'Female',
    'Other'
);


ALTER TYPE public.gender_enum OWNER TO root;

--
-- TOC entry 879 (class 1247 OID 16412)
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
-- TOC entry 219 (class 1259 OID 16421)
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
-- TOC entry 220 (class 1259 OID 16432)
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
-- TOC entry 3580 (class 0 OID 0)
-- Dependencies: 220
-- Name: courses_course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.courses_course_id_seq OWNED BY public.courses.course_id;


--
-- TOC entry 221 (class 1259 OID 16433)
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
-- TOC entry 222 (class 1259 OID 16439)
-- Name: departments; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.departments (
    dept_id integer NOT NULL,
    name text NOT NULL,
    code text NOT NULL
);


ALTER TABLE public.departments OWNER TO root;

--
-- TOC entry 223 (class 1259 OID 16447)
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
-- TOC entry 3581 (class 0 OID 0)
-- Dependencies: 223
-- Name: departments_dept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.departments_dept_id_seq OWNED BY public.departments.dept_id;


--
-- TOC entry 224 (class 1259 OID 16448)
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
-- TOC entry 225 (class 1259 OID 16454)
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
-- TOC entry 226 (class 1259 OID 16461)
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
-- TOC entry 3582 (class 0 OID 0)
-- Dependencies: 226
-- Name: employees_employee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.employees_employee_id_seq OWNED BY public.employees.employee_id;


--
-- TOC entry 227 (class 1259 OID 16462)
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
-- TOC entry 228 (class 1259 OID 16471)
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
-- TOC entry 3583 (class 0 OID 0)
-- Dependencies: 228
-- Name: majors_major_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.majors_major_id_seq OWNED BY public.majors.major_id;


--
-- TOC entry 229 (class 1259 OID 16472)
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
-- TOC entry 230 (class 1259 OID 16482)
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
-- TOC entry 3584 (class 0 OID 0)
-- Dependencies: 230
-- Name: persons_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.persons_person_id_seq OWNED BY public.persons.person_id;


--
-- TOC entry 231 (class 1259 OID 16483)
-- Name: positions; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.positions (
    position_id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.positions OWNER TO root;

--
-- TOC entry 232 (class 1259 OID 16490)
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
-- TOC entry 3585 (class 0 OID 0)
-- Dependencies: 232
-- Name: positions_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.positions_position_id_seq OWNED BY public.positions.position_id;


--
-- TOC entry 233 (class 1259 OID 16491)
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
-- TOC entry 234 (class 1259 OID 16498)
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
-- TOC entry 235 (class 1259 OID 16505)
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
-- TOC entry 3586 (class 0 OID 0)
-- Dependencies: 235
-- Name: students_student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.students_student_id_seq OWNED BY public.students.student_id;


--
-- TOC entry 237 (class 1259 OID 16598)
-- Name: users; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    employee_id integer NOT NULL,
    username text NOT NULL,
    password_hash text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO root;

--
-- TOC entry 236 (class 1259 OID 16597)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

ALTER TABLE public.users ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3348 (class 2604 OID 16506)
-- Name: courses course_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.courses ALTER COLUMN course_id SET DEFAULT nextval('public.courses_course_id_seq'::regclass);


--
-- TOC entry 3349 (class 2604 OID 16507)
-- Name: departments dept_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.departments ALTER COLUMN dept_id SET DEFAULT nextval('public.departments_dept_id_seq'::regclass);


--
-- TOC entry 3350 (class 2604 OID 16508)
-- Name: employees employee_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employees ALTER COLUMN employee_id SET DEFAULT nextval('public.employees_employee_id_seq'::regclass);


--
-- TOC entry 3351 (class 2604 OID 16509)
-- Name: majors major_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.majors ALTER COLUMN major_id SET DEFAULT nextval('public.majors_major_id_seq'::regclass);


--
-- TOC entry 3352 (class 2604 OID 16510)
-- Name: persons person_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persons ALTER COLUMN person_id SET DEFAULT nextval('public.persons_person_id_seq'::regclass);


--
-- TOC entry 3353 (class 2604 OID 16511)
-- Name: positions position_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.positions ALTER COLUMN position_id SET DEFAULT nextval('public.positions_position_id_seq'::regclass);


--
-- TOC entry 3355 (class 2604 OID 16512)
-- Name: students student_id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.students ALTER COLUMN student_id SET DEFAULT nextval('public.students_student_id_seq'::regclass);


--
-- TOC entry 3556 (class 0 OID 16421)
-- Dependencies: 219
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3558 (class 0 OID 16433)
-- Dependencies: 221
-- Data for Name: department_heads; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3559 (class 0 OID 16439)
-- Dependencies: 222
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3561 (class 0 OID 16448)
-- Dependencies: 224
-- Data for Name: employee_positions; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3562 (class 0 OID 16454)
-- Dependencies: 225
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3564 (class 0 OID 16462)
-- Dependencies: 227
-- Data for Name: majors; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3566 (class 0 OID 16472)
-- Dependencies: 229
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3568 (class 0 OID 16483)
-- Dependencies: 231
-- Data for Name: positions; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3570 (class 0 OID 16491)
-- Dependencies: 233
-- Data for Name: student_majors; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3571 (class 0 OID 16498)
-- Dependencies: 234
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3574 (class 0 OID 16598)
-- Dependencies: 237
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: root
--



--
-- TOC entry 3587 (class 0 OID 0)
-- Dependencies: 220
-- Name: courses_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.courses_course_id_seq', 1, false);


--
-- TOC entry 3588 (class 0 OID 0)
-- Dependencies: 223
-- Name: departments_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.departments_dept_id_seq', 1, false);


--
-- TOC entry 3589 (class 0 OID 0)
-- Dependencies: 226
-- Name: employees_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.employees_employee_id_seq', 1, false);


--
-- TOC entry 3590 (class 0 OID 0)
-- Dependencies: 228
-- Name: majors_major_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.majors_major_id_seq', 1, false);


--
-- TOC entry 3591 (class 0 OID 0)
-- Dependencies: 230
-- Name: persons_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.persons_person_id_seq', 1, false);


--
-- TOC entry 3592 (class 0 OID 0)
-- Dependencies: 232
-- Name: positions_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.positions_position_id_seq', 1, false);


--
-- TOC entry 3593 (class 0 OID 0)
-- Dependencies: 235
-- Name: students_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.students_student_id_seq', 1, false);


--
-- TOC entry 3594 (class 0 OID 0)
-- Dependencies: 236
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- TOC entry 3359 (class 2606 OID 16514)
-- Name: courses courses_course_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_course_code_key UNIQUE (course_code);


--
-- TOC entry 3361 (class 2606 OID 16516)
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (course_id);


--
-- TOC entry 3365 (class 2606 OID 16518)
-- Name: departments departments_code_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_code_key UNIQUE (code);


--
-- TOC entry 3367 (class 2606 OID 16520)
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (dept_id);


--
-- TOC entry 3369 (class 2606 OID 16522)
-- Name: employee_positions employee_positions_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employee_positions
    ADD CONSTRAINT employee_positions_pkey PRIMARY KEY (employee_id, position_id, start_date);


--
-- TOC entry 3371 (class 2606 OID 16524)
-- Name: employees employees_person_id_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_person_id_key UNIQUE (person_id);


--
-- TOC entry 3373 (class 2606 OID 16526)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (employee_id);


--
-- TOC entry 3375 (class 2606 OID 16528)
-- Name: majors majors_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.majors
    ADD CONSTRAINT majors_pkey PRIMARY KEY (major_id);


--
-- TOC entry 3377 (class 2606 OID 16530)
-- Name: persons persons_email_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_email_key UNIQUE (email);


--
-- TOC entry 3379 (class 2606 OID 16532)
-- Name: persons persons_pesel_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pesel_key UNIQUE (pesel);


--
-- TOC entry 3381 (class 2606 OID 16534)
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (person_id);


--
-- TOC entry 3383 (class 2606 OID 16536)
-- Name: positions positions_name_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_name_key UNIQUE (name);


--
-- TOC entry 3385 (class 2606 OID 16538)
-- Name: positions positions_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_pkey PRIMARY KEY (position_id);


--
-- TOC entry 3387 (class 2606 OID 16540)
-- Name: student_majors student_majors_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.student_majors
    ADD CONSTRAINT student_majors_pkey PRIMARY KEY (student_id, major_id, start_date);


--
-- TOC entry 3389 (class 2606 OID 16542)
-- Name: students students_person_id_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_person_id_key UNIQUE (person_id);


--
-- TOC entry 3391 (class 2606 OID 16544)
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (student_id);


--
-- TOC entry 3393 (class 2606 OID 16612)
-- Name: users users_employee_id_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_employee_id_key UNIQUE (employee_id);


--
-- TOC entry 3395 (class 2606 OID 16610)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 3397 (class 2606 OID 16614)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 3362 (class 1259 OID 16545)
-- Name: idx_courses_course_code; Type: INDEX; Schema: public; Owner: root
--

CREATE INDEX idx_courses_course_code ON public.courses USING btree (course_code);


--
-- TOC entry 3363 (class 1259 OID 16546)
-- Name: one_active_head_per_department; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX one_active_head_per_department ON public.department_heads USING btree (dept_id) WHERE (end_date IS NULL);


--
-- TOC entry 3398 (class 2606 OID 16547)
-- Name: courses fk_courses_department; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT fk_courses_department FOREIGN KEY (dept_id) REFERENCES public.departments(dept_id) ON DELETE CASCADE;


--
-- TOC entry 3399 (class 2606 OID 16552)
-- Name: department_heads fk_dh_department; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.department_heads
    ADD CONSTRAINT fk_dh_department FOREIGN KEY (dept_id) REFERENCES public.departments(dept_id) ON DELETE CASCADE;


--
-- TOC entry 3400 (class 2606 OID 16557)
-- Name: department_heads fk_dh_employee; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.department_heads
    ADD CONSTRAINT fk_dh_employee FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id);


--
-- TOC entry 3403 (class 2606 OID 16562)
-- Name: employees fk_employees_person; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT fk_employees_person FOREIGN KEY (person_id) REFERENCES public.persons(person_id) ON DELETE CASCADE;


--
-- TOC entry 3401 (class 2606 OID 16567)
-- Name: employee_positions fk_ep_employee; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employee_positions
    ADD CONSTRAINT fk_ep_employee FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id) ON DELETE CASCADE;


--
-- TOC entry 3402 (class 2606 OID 16572)
-- Name: employee_positions fk_ep_position; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.employee_positions
    ADD CONSTRAINT fk_ep_position FOREIGN KEY (position_id) REFERENCES public.positions(position_id);


--
-- TOC entry 3404 (class 2606 OID 16577)
-- Name: majors fk_majors_department; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.majors
    ADD CONSTRAINT fk_majors_department FOREIGN KEY (dept_id) REFERENCES public.departments(dept_id) ON DELETE CASCADE;


--
-- TOC entry 3405 (class 2606 OID 16582)
-- Name: student_majors fk_sm_major; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.student_majors
    ADD CONSTRAINT fk_sm_major FOREIGN KEY (major_id) REFERENCES public.majors(major_id) ON DELETE CASCADE;


--
-- TOC entry 3406 (class 2606 OID 16587)
-- Name: student_majors fk_sm_student; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.student_majors
    ADD CONSTRAINT fk_sm_student FOREIGN KEY (student_id) REFERENCES public.students(student_id) ON DELETE CASCADE;


--
-- TOC entry 3407 (class 2606 OID 16592)
-- Name: students fk_students_person; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT fk_students_person FOREIGN KEY (person_id) REFERENCES public.persons(person_id) ON DELETE CASCADE;


--
-- TOC entry 3408 (class 2606 OID 16615)
-- Name: users fk_users_employee; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_employee FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id) ON DELETE CASCADE;


-- Completed on 2026-01-08 17:43:25 UTC

--
-- PostgreSQL database dump complete
--

\unrestrict meYmOz8vfKkVfbbOQDlMQ2CQeT7dGqUDyO4oyu87q4YPavejjCIUPwitCZoF2z9

