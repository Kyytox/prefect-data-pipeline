-- Create the database
CREATE DATABASE {{ cookiecutter.database_name }}
	WITH OWNER = {{ cookiecutter.database_user }}
	ENCODING = 'UTF8';