-- Table: public.responsible_persons

-- DROP TABLE IF EXISTS public.responsible_persons;

CREATE TABLE IF NOT EXISTS public.responsible_persons
(
	responsible_person_id INT GENERATED ALWAYS AS IDENTITY, 
	first_name VARCHAR(30) NOT NULL, 
	last_name VARCHAR(30) NOT NULL, 
	phone_number phone_number NOT NULL,
	email email_address NOT NULL, 
	PRIMARY KEY (responsible_person_id),
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.responsible_persons
    OWNER to postgres;