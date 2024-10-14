-- Filament tables for spools

CREATE TABLE filament_types (
	filament_type_id	SERIAL PRIMARY KEY,
	filament_type 		TEXT UNIQUE NOT NULL
);


CREATE TABLE filament_colors (
	filament_color_id	SERIAL PRIMARY KEY,
	color			TEXT UNIQUE NOT NULL
);


CREATE TABLE manufacturer (
	manufacturer_id		SERIAL PRIMARY KEY,
	name			TEXT UNIQUE NOT NULL
);



CREATE TABLE filaments (
	filament_id 		SERIAL PRIMARY KEY,
	filament_type 		INTEGER REFERENCES filament_types(filament_type_id) NOT NULL,
	filament_color		INTEGER REFERENCES filament_colors(filament_color_id) NOT NULL,
	filament_manufacturer	INTEGER REFERENCES manufacturer(manufacturer_id) NOT NULL
);




-- Printer tables?
/*
CREATE TABLE printers (
	printer_id 		SERIAL PRIMARY KEY,
	filament		int REFERENCES filaments(filament_id)
	current_job
);
*/

CREATE TABLE gcode_files (
	file_id			SERIAL PRIMARY KEY,
	gcode_text		TEXT NOT NULL
);



-- Enum for jab status
-- PENDING - Striaghtforward, this is default when a job is not assigned to any printers yet
-- IP (In Progress) - Job has been assigned to a printer
-- RHI (Requires Human Intervention) - An error has occured and the print cannot continue, requires human intervention
-- COMPLETE - Job has been FULLY COMPLETED AND TAKEN OFF THE BASE PLATE, job can safely be moved to a different table
CREATE TYPE status_code AS ENUM('PENDING', 'IP', 'RHI', 'COMPLETE');


-- Jobs table

CREATE TABLE jobs (
	job_id			SERIAL PRIMARY KEY,
	order_id		INTEGER NOT NULL,
		CONSTRAINT order_id CHECK (order_id >= 0),
	quantity		INTEGER NOT NULL,
	job_name		TEXT UNIQUE NOT NULL,
	job_status		status_code NOT NULL DEFAULT 'PENDING',
	status_message		TEXT,
	printer_assignment 	INTEGER NOT NULL,
	CONSTRAINT printer_assignment CHECK (printer_assignment >= 0),
	nozzle_size		INTEGER NOT NULL,
	filament_id		INTEGER REFERENCES filaments(filament_id),
	file_id			INTEGER REFERENCES gcode_files(file_id),
	created_on		TIMESTAMP(3) DEFAULT NOW() NOT NULL
);


CREATE VIEW job_info AS SELECT
	jobs.order_id,
	jobs.quantity,
	jobs.job_name,
	jobs.job_status,
	jobs.status_message,
	jobs.printer_assignment,
	jobs.nozzle_size,
	filament_types.filament_type,
	filament_colors.color
FROM jobs
INNER JOIN filaments
ON jobs.filament_id = filaments.filament_id
INNER JOIN filament_types
ON filaments.filament_type = filament_types.filament_type_id
INNER JOIN filament_colors
ON filaments.filament_color = filament_colors.filament_color_id;



