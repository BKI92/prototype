-- Table: public.users
CREATE TABLE IF NOT EXISTS public.users(
    pk serial,
    username text,
    tg_id integer,
    description text,
    created timestamp with time zone NOT NULL,
    is_active bool NOT NULL DEFAULT TRUE,
    CONSTRAINT users_pkey PRIMARY KEY (pk)
);

-- Table: public.celebrities
CREATE TABLE IF NOT EXISTS public.celebrities(
    pk serial,
    name text,
    description text,
    created timestamp with time zone NOT NULL,
    CONSTRAINT celebrities_pkey PRIMARY KEY (pk)
);


-- Table: public.messages
CREATE TABLE IF NOT EXISTS public.messages(
    user_pk integer,
    celebrity_pk integer,
    title text,
    created timestamp with time zone NOT NULL
);

ALTER TABLE public.messages ADD CONSTRAINT messages_fkey_users
    FOREIGN KEY (user_pk) REFERENCES public.users (pk)
    ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID;

ALTER TABLE public.messages ADD CONSTRAINT messages_fkey_celebrities
    FOREIGN KEY (celebrity_pk) REFERENCES public.celebrities (pk)
    ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID;


CREATE INDEX  idndex_messages_1 ON messages (user_pk, created);