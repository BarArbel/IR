-- Table: public.files

-- DROP TABLE public.files;
CREATE SCHEMA IF NOT EXISTS retrieval;

CREATE TABLE IF NOT EXISTS retrieval.files(
	f_id BIGSERIAL PRIMARY KEY NOT NULL,
	f_name TEXT NOT NULL,
	f_author TEXT NOT NULL,
	f_type TEXT NOT NULL,
	hidden BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS retrieval.inverted_index(
	word TEXT PRIMARY KEY NOT NULL,
	docs_num BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS retrieval.posting_file(
	word TEXT NOT NULL,
	f_id BIGINT NOT NULL,
	hits_num BIGINT NOT NULL,
	PRIMARY KEY(word, f_id)
);

CREATE TABLE IF NOT EXISTS retrieval.stop_words(
	word TEXT PRIMARY KEY NOT NULL
);