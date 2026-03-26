DROP TABLE employees;
DROP TABLE departments;
DROP TABLE salary_audit;
DROP TABLE employee_log;

CREATE TABLE employees (
    employee_id       INT           PRIMARY KEY,
    full_name         VARCHAR(100)  NOT NULL,
    department_id     INT,          -- 1=Engineering  2=Marketing  3=HR
                                    -- 4=Sales        5=Finance
    job_title         VARCHAR(50),
    salary            DECIMAL(10,2),
    hire_date         DATE,
    is_active         BOOLEAN       DEFAULT TRUE,
    performance_score DECIMAL(3,1), -- score out of 10
    bonus_percent     DECIMAL(5,2), -- NULL means no bonus
    email             VARCHAR(100)  UNIQUE
);

INSERT INTO employees VALUES
 (1,  'Alice Johnson', 1, 'Senior Engineer',  95000.00,
      '2018-03-15', TRUE,  9.2, 15.00, 'alice@company.com'),
 (2,  'Bob Smith',     1, 'Junior Engineer',  62000.00,
      '2021-07-01', TRUE,  7.4,  8.00, 'bob@company.com'),
 (3,  'Carol White',   2, 'Marketing Lead',   78000.00,
      '2019-11-20', TRUE,  8.8, 12.00, 'carol@company.com'),
 (4,  'David Brown',   2, 'Analyst',          55000.00,
      '2022-01-10', TRUE,  6.5,  5.00, 'david@company.com'),
 (5,  'Eva Green',     3, 'HR Manager',       82000.00,
      '2017-06-05', TRUE,  9.0, 13.00, 'eva@company.com'),
 (6,  'Frank Lee',     3, 'HR Specialist',    50000.00,
      '2023-03-22', TRUE,  7.1,  6.00, 'frank@company.com'),
 (7,  'Grace Kim',     1, 'Tech Lead',       110000.00,
      '2015-09-30', TRUE,  9.7, 18.00, 'grace@company.com'),
 (8,  'Henry Adams',   4, 'Sales Executive',  67000.00,
      '2020-05-14', TRUE,  7.8, 10.00, 'henry@company.com'),
 (9,  'Iris Patel',    4, 'Sales Intern',     38000.00,
      '2023-08-01', FALSE, 6.0,  NULL, 'iris@company.com'),
 (10, 'James Turner',  5, 'Finance Manager',  91000.00,
      '2016-12-01', FALSE, 8.3, 14.00, 'james@company.com');


CREATE TABLE departments (
    department_id   INT PRIMARY KEY,
    dept_name       VARCHAR(50) NOT NULL,
    location        VARCHAR(50),
    budget          DECIMAL(12, 2)
);



INSERT INTO departments VALUES
(1, 'Engineering', 'New York',     500000.00),
(2, 'Marketing',   'Chicago',      200000.00),
(3, 'HR',          'Austin',       150000.00),
(4, 'Sales',       'Dallas',       300000.00),
(5, 'Finance',     'New York',     250000.00),
(6, 'Legal',       'San Francisco', 180000.00);  


CREATE TABLE salary_audit (
    audit_id      INT          PRIMARY KEY,
    employee_id   INT           NOT NULL,
    old_salary    DECIMAL(10,2),
    new_salary    DECIMAL(10,2),
    changed_at    DATETIME      DEFAULT CURRENT_TIMESTAMP -- use DATE if needed
);


CREATE TABLE employee_log (
    log_id        INT         PRIMARY KEY,
    employee_id   INT           NOT NULL,
    full_name     VARCHAR(100),
    action        VARCHAR(20),  -- 'INSERTED' or 'DELETED'
    action_time   DATETIME      DEFAULT CURRENT_TIMESTAMP -- use DATE if needed
);


SELECT * FROM employees;
SELECT * FROM departments;

CREATE OR REPLACE PROCEDURE print_all_employees()
LANGUAGE plpgsql
AS $$
DECLARE 
    v_name VARCHAR(100);
    v_sal DECIMAL(10,2);
    cur CURSOR FOR SELECT full_name, salary FROM employees;
BEGIN
    OPEN cur;
    LOOP
    FETCH cur INTO v_name, v_sal;
    EXIT WHEN NOT FOUND;
    RAISE NOTICE 'Employee: %, Salary: %', v_name, v_sal;
    END LOOP;
    CLOSE cur;
END $$;
CALL print_all_employees();



SELECT d.dept_name, COUNT(e.employee_id) AS total_employees
FROM employees e
JOIN departments d ON e.department_id=d.department_id
GROUP BY d.dept_name
ORDER BY total_employees DESC;


