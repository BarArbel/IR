-- Table: public.files

-- DROP TABLE public.files;
CREATE SCHEMA IF NOT EXISTS retrieval;

CREATE TABLE retrieval.files(
	f_id BIGSERIAL PRIMARY KEY NOT NULL,
	f_name TEXT NOT NULL,
	hidden BOOLEAN NOT NULL
);

CREATE TABLE retrieval.inverted_index(
	word TEXT PRIMARY KEY NOT NULL,
	docs_num BIGINT NOT NULL,
	files_table_name TEXT NOT NULL
);

CREATE TABLE retrieval.stop_list(
	word TEXT PRIMARY KEY NOT NULL
);
