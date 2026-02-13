--
-- PostgreSQL database dump
--

\restrict uapmXiwk13EhuzAZzBTCu2rt6quvef1rYh9PdzEYpdoinklNYPmFmbChwfH8CYL

-- Dumped from database version 16.11
-- Dumped by pg_dump version 16.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: genderenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.genderenum AS ENUM (
    'STALLION',
    'MARE',
    'GELDING'
);


ALTER TYPE public.genderenum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: horses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.horses (
    id integer NOT NULL,
    nickname character varying(100) NOT NULL,
    gender public.genderenum NOT NULL,
    age integer NOT NULL,
    owner_id integer NOT NULL
);


ALTER TABLE public.horses OWNER TO postgres;

--
-- Name: horses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.horses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.horses_id_seq OWNER TO postgres;

--
-- Name: horses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.horses_id_seq OWNED BY public.horses.id;


--
-- Name: jockeys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jockeys (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    address character varying(500) NOT NULL,
    age integer NOT NULL,
    rating integer NOT NULL
);


ALTER TABLE public.jockeys OWNER TO postgres;

--
-- Name: jockeys_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jockeys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jockeys_id_seq OWNER TO postgres;

--
-- Name: jockeys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jockeys_id_seq OWNED BY public.jockeys.id;


--
-- Name: owners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.owners (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    address character varying(500) NOT NULL,
    phone character varying(20) NOT NULL
);


ALTER TABLE public.owners OWNER TO postgres;

--
-- Name: owners_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.owners_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.owners_id_seq OWNER TO postgres;

--
-- Name: owners_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.owners_id_seq OWNED BY public.owners.id;


--
-- Name: race_participants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.race_participants (
    id integer NOT NULL,
    race_id integer NOT NULL,
    jockey_id integer NOT NULL,
    horse_id integer NOT NULL,
    place integer NOT NULL,
    time_result time without time zone
);


ALTER TABLE public.race_participants OWNER TO postgres;

--
-- Name: race_participants_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.race_participants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.race_participants_id_seq OWNER TO postgres;

--
-- Name: race_participants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.race_participants_id_seq OWNED BY public.race_participants.id;


--
-- Name: races; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.races (
    id integer NOT NULL,
    date date NOT NULL,
    "time" time without time zone NOT NULL,
    hippodrome character varying(200) NOT NULL,
    name character varying(200)
);


ALTER TABLE public.races OWNER TO postgres;

--
-- Name: races_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.races_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.races_id_seq OWNER TO postgres;

--
-- Name: races_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.races_id_seq OWNED BY public.races.id;


--
-- Name: weather; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.weather (
    id integer NOT NULL,
    date date NOT NULL,
    "time" time without time zone NOT NULL
);


ALTER TABLE public.weather OWNER TO postgres;

--
-- Name: weather_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.weather_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weather_id_seq OWNER TO postgres;

--
-- Name: weather_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.weather_id_seq OWNED BY public.weather.id;


--
-- Name: horses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horses ALTER COLUMN id SET DEFAULT nextval('public.horses_id_seq'::regclass);


--
-- Name: jockeys id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jockeys ALTER COLUMN id SET DEFAULT nextval('public.jockeys_id_seq'::regclass);


--
-- Name: owners id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.owners ALTER COLUMN id SET DEFAULT nextval('public.owners_id_seq'::regclass);


--
-- Name: race_participants id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.race_participants ALTER COLUMN id SET DEFAULT nextval('public.race_participants_id_seq'::regclass);


--
-- Name: races id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.races ALTER COLUMN id SET DEFAULT nextval('public.races_id_seq'::regclass);


--
-- Name: weather id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weather ALTER COLUMN id SET DEFAULT nextval('public.weather_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: horses horses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horses
    ADD CONSTRAINT horses_pkey PRIMARY KEY (id);


--
-- Name: jockeys jockeys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jockeys
    ADD CONSTRAINT jockeys_pkey PRIMARY KEY (id);


--
-- Name: owners owners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.owners
    ADD CONSTRAINT owners_pkey PRIMARY KEY (id);


--
-- Name: race_participants race_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.race_participants
    ADD CONSTRAINT race_participants_pkey PRIMARY KEY (id);


--
-- Name: races races_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.races
    ADD CONSTRAINT races_pkey PRIMARY KEY (id);


--
-- Name: weather weather_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weather
    ADD CONSTRAINT weather_pkey PRIMARY KEY (id);


--
-- Name: idx_horse_races; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_horse_races ON public.race_participants USING btree (horse_id);


--
-- Name: idx_jockey_races; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_jockey_races ON public.race_participants USING btree (jockey_id);


--
-- Name: idx_race_place; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_race_place ON public.race_participants USING btree (race_id, place);


--
-- Name: ix_horses_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_horses_id ON public.horses USING btree (id);


--
-- Name: ix_jockeys_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_jockeys_id ON public.jockeys USING btree (id);


--
-- Name: ix_owners_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_owners_id ON public.owners USING btree (id);


--
-- Name: ix_race_participants_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_race_participants_id ON public.race_participants USING btree (id);


--
-- Name: ix_races_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_races_date ON public.races USING btree (date);


--
-- Name: ix_races_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_races_id ON public.races USING btree (id);


--
-- Name: ix_weather_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_weather_id ON public.weather USING btree (id);


--
-- Name: horses horses_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horses
    ADD CONSTRAINT horses_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.owners(id);


--
-- Name: race_participants race_participants_horse_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.race_participants
    ADD CONSTRAINT race_participants_horse_id_fkey FOREIGN KEY (horse_id) REFERENCES public.horses(id);


--
-- Name: race_participants race_participants_jockey_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.race_participants
    ADD CONSTRAINT race_participants_jockey_id_fkey FOREIGN KEY (jockey_id) REFERENCES public.jockeys(id);


--
-- Name: race_participants race_participants_race_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.race_participants
    ADD CONSTRAINT race_participants_race_id_fkey FOREIGN KEY (race_id) REFERENCES public.races(id);


--
-- PostgreSQL database dump complete
--

\unrestrict uapmXiwk13EhuzAZzBTCu2rt6quvef1rYh9PdzEYpdoinklNYPmFmbChwfH8CYL

