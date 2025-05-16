-- Connect to the specific database
\c {{ cookiecutter.database_name }};

-- Create the rockets table with launch data
CREATE TABLE raw_rockets (
	launch_id VARCHAR(255) PRIMARY KEY,
	launch_date TIMESTAMP NOT NULL,
	name VARCHAR(255) NOT NULL,
	status VARCHAR(255),
	launch_service_provider VARCHAR(255),
	launch_site VARCHAR(255),
	country VARCHAR(255),
	rocket VARCHAR(255),
	mission VARCHAR(255),
	mission_type VARCHAR(255)
);