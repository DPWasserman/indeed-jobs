CREATE TABLE company (
	id INT IDENTITY(1,1) PRIMARY KEY,
	company_name NVARCHAR(100) UNIQUE,
	company_url VARCHAR(255), -- Indeed URL for the company
	num_stars NUMERIC(3,2), -- #.# stars out of 5
	num_reviews SMALLINT,
	create_date SMALLDATETIME DEFAULT CURRENT_TIMESTAMP,
	update_date SMALLDATETIME DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE job (
	id INT IDENTITY(1,1) PRIMARY KEY,
	indeed_job_key VARCHAR(20) UNIQUE, -- To go to the indeed.com page, https://www.indeed.com/viewjob?jk={indeed_job_key}
	job_title NVARCHAR(100) NOT NULL,
	company_id INT NOT NULL,
	job_location NVARCHAR(50),
	job_description NVARCHAR(MAX),
	original_url VARCHAR(255),
	job_salary_low NUMERIC(7,0), -- Low range of the annual job salary in USD
	job_salary_high NUMERIC(7,0), -- High range of the annual job salary in USD
	post_date DATE,
	create_date SMALLDATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (company_id)
		REFERENCES company(id) ON DELETE CASCADE
)