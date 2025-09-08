-- Table: public.FeedItem

-- DROP TABLE IF EXISTS public."FeedItem";

CREATE TABLE IF NOT EXISTS public."FeedItem"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    title text COLLATE pg_catalog."default",
    url text COLLATE pg_catalog."default",
    content text COLLATE pg_catalog."default",
    date timestamp without time zone,
    webcontent text COLLATE pg_catalog."default",
    category text COLLATE pg_catalog."default",
    CONSTRAINT "FeedItem_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."FeedItem"
    OWNER to postgres;