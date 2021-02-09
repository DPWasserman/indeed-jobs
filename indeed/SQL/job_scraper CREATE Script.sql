CREATE TABLE company (
	id INT IDENTITY(1,1) PRIMARY KEY,
	company_name NVARCHAR(100) UNIQUE,
	company_url VARCHAR(255), -- Indeed URL for the company
	num_stars NUMERIC(3,2), -- #.# stars out of 5
	num_reviews SMALLINT, -- number of people who gave a review
	create_date SMALLDATETIME DEFAULT CURRENT_TIMESTAMP,
	update_date SMALLDATETIME DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE job (
	id INT IDENTITY(1,1) PRIMARY KEY,
	indeed_job_key VARCHAR(20) UNIQUE, -- To go to the indeed.com page, https://www.indeed.com/viewjob?jk={indeed_job_key}
	job_title NVARCHAR(100) NOT NULL, -- title of the job at the company (from the posting)
	company_id INT NOT NULL, -- foreign key to company table
	search_location VARCHAR(50), -- search string used to find the job
	job_location NVARCHAR(50), -- where the job is located (Could be REMOTE)
	job_description NVARCHAR(MAX), -- text of the job description in the posting on indeed.com
	search_page_url VARCHAR(255), -- page on which the job was found
	original_url VARCHAR(255), -- link to the post on the original job site (before put on indeed.com)
	salary_txt VARCHAR(50), -- text that had the salary information
	job_salary_low NUMERIC(7,0), -- Low range of the annual job salary in USD
	job_salary_high NUMERIC(7,0), -- High range of the annual job salary in USD
	post_date DATE, -- date the job was listed on indeed.com
	create_date SMALLDATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (company_id)
		REFERENCES company(id) ON DELETE CASCADE
)