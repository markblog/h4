
-------------------------------------------------------------------------------------------------------
-- Step 1: Drop all db objects
-------------------------------------------------------------------------------------------------------
DROP SCHEMA IF EXISTS membership CASCADE;
DROP SCHEMA IF EXISTS meta CASCADE;
DROP SCHEMA IF EXISTS public CASCADE;

-------------------------------------------------------------------------------------------------------
-- Step 2: Recreate all db objects
-------------------------------------------------------------------------------------------------------
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA membership;
ALTER SCHEMA membership OWNER TO postgres;

CREATE SCHEMA meta;
ALTER SCHEMA meta OWNER TO postgres;

CREATE SCHEMA public;
ALTER SCHEMA public OWNER TO postgres;


CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';

CREATE EXTENSION IF NOT EXISTS pgcrypto with schema membership;

SET search_path = public, pg_catalog;


CREATE FUNCTION export_to_csv(tablename text, folder_path text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE STATEMENT TEXT;
BEGIN
  STATEMENT := format('COPY %s TO ''%s%s.csv'' WITH CSV HEADER', tablename, folder_path, tablename);
  EXECUTE STATEMENT;
END;
$$;
ALTER FUNCTION public.export_to_csv(tablename text, folder_path text) OWNER TO postgres;


CREATE FUNCTION export_tables_to_csv(folder_path text) RETURNS void
    LANGUAGE plpgsql
    AS $$ 
BEGIN
  PERFORM export_to_csv('membership.organization', folder_path);
  PERFORM export_to_csv('membership.login', folder_path);
  PERFORM export_to_csv('membership.session', folder_path);
  PERFORM export_to_csv('public.data_provider', folder_path);
  PERFORM export_to_csv('public.esg_rating', folder_path);
  PERFORM export_to_csv('public.esg_factor', folder_path);
  PERFORM export_to_csv('public.weight_method', folder_path);
  PERFORM export_to_csv('public.exchange_rate', folder_path);
  PERFORM export_to_csv('public.geography', folder_path);
  PERFORM export_to_csv('public.sector', folder_path);
  PERFORM export_to_csv('public.correlation_group', folder_path);
  PERFORM export_to_csv('public.asset_type', folder_path);
  PERFORM export_to_csv('public.company', folder_path);
  PERFORM export_to_csv('public.company_esg_factor', folder_path);
  PERFORM export_to_csv('public.company_esg_summary', folder_path);
  PERFORM export_to_csv('public.company_supplier', folder_path);
  PERFORM export_to_csv('public.company_asset', folder_path);
  PERFORM export_to_csv('public.security', folder_path);
  PERFORM export_to_csv('public.company_primary_security', folder_path);
  PERFORM export_to_csv('public.security_financial_series', folder_path);
  PERFORM export_to_csv('public.portfolio', folder_path);
  PERFORM export_to_csv('public.portfolio_security', folder_path);
  PERFORM export_to_csv('public.portfolio_security_value', folder_path);
  PERFORM export_to_csv('public.portfolio_result', folder_path);
  PERFORM export_to_csv('public.portfolio_esg_score', folder_path);
  PERFORM export_to_csv('public.grouping', folder_path);
  PERFORM export_to_csv('public.metric', folder_path);
  PERFORM export_to_csv('public.portfolio_metric_date', folder_path);
  PERFORM export_to_csv('public.portfolio_grouping_metric', folder_path);
  PERFORM export_to_csv('public.security_esg_factor', folder_path);
  PERFORM export_to_csv('public.tag_history', folder_path);
  PERFORM export_to_csv('public.alert_type', folder_path);
  PERFORM export_to_csv('public.alert_history', folder_path);
  PERFORM export_to_csv('public.alert_substitution_value', folder_path);
  PERFORM export_to_csv('public.alert_search_tag', folder_path);
  PERFORM export_to_csv('public.alert_digest_history', folder_path);
  PERFORM export_to_csv('meta.tag_category', folder_path);
  PERFORM export_to_csv('meta.tag_type', folder_path);
  PERFORM export_to_csv('meta.fixed_tag', folder_path);
END;
$$;
ALTER FUNCTION public.export_tables_to_csv(folder_path text) OWNER TO postgres;


CREATE FUNCTION import_from_csv(tablename text, folder_path text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE STATEMENT TEXT;
BEGIN
  STATEMENT := format('COPY %s FROM ''%s%s.csv'' WITH CSV HEADER', tablename, folder_path, tablename);
  EXECUTE STATEMENT;
END;
$$;
ALTER FUNCTION public.import_from_csv(tablename text, folder_path text) OWNER TO postgres;


CREATE FUNCTION import_tables_from_csv(folder_path text) RETURNS void
    LANGUAGE plpgsql
    AS $$ 
BEGIN
  PERFORM import_from_csv('membership.organization', folder_path);
  PERFORM setval('membership.organization_id_seq', (SELECT MAX(id) FROM membership.organization));
  PERFORM import_from_csv('membership.login', folder_path);
  PERFORM setval('membership.login_id_seq', (SELECT MAX(id) FROM membership.login));
  PERFORM import_from_csv('membership.session', folder_path);
  PERFORM import_from_csv('public.data_provider', folder_path);
  PERFORM import_from_csv('public.esg_rating', folder_path);
  PERFORM import_from_csv('public.esg_factor', folder_path);
  PERFORM import_from_csv('public.weight_method', folder_path);
  PERFORM import_from_csv('public.exchange_rate', folder_path);
  PERFORM import_from_csv('public.geography', folder_path);
  PERFORM import_from_csv('public.sector', folder_path);
  PERFORM import_from_csv('public.correlation_group', folder_path);
  PERFORM setval('public.correlation_group_id_seq', (SELECT MAX(id) FROM public.correlation_group));
  PERFORM import_from_csv('public.asset_type', folder_path);
  PERFORM import_from_csv('public.company', folder_path);
  PERFORM import_from_csv('public.company_esg_factor', folder_path);
  PERFORM import_from_csv('public.company_esg_summary', folder_path);
  PERFORM import_from_csv('public.company_supplier', folder_path);
  PERFORM import_from_csv('public.company_asset', folder_path);
  PERFORM import_from_csv('public.security', folder_path);
  PERFORM import_from_csv('public.company_primary_security', folder_path);
  PERFORM import_from_csv('public.security_financial_series', folder_path);
  PERFORM import_from_csv('public.portfolio', folder_path);
  PERFORM setval('public.portfolio_id_seq', (SELECT MAX(id) FROM public.portfolio));
  PERFORM import_from_csv('public.portfolio_security', folder_path);
  PERFORM import_from_csv('public.portfolio_security_value', folder_path);
  PERFORM import_from_csv('public.portfolio_result', folder_path);
  PERFORM import_from_csv('public.portfolio_esg_score', folder_path);
  PERFORM import_from_csv('public.grouping', folder_path);
  PERFORM import_from_csv('public.metric', folder_path);
  PERFORM import_from_csv('public.portfolio_metric_date', folder_path);
  PERFORM setval('public.portfolio_metric_date_id_seq', (SELECT MAX(id) FROM public.portfolio_metric_date));
  PERFORM import_from_csv('public.portfolio_grouping_metric', folder_path);
  PERFORM import_from_csv('public.security_esg_factor', folder_path);
  PERFORM import_from_csv('public.tag_history', folder_path);
  PERFORM setval('public.tag_history_id_seq', (SELECT MAX(id) FROM public.tag_history));
  PERFORM import_from_csv('public.alert_type', folder_path);
  PERFORM setval('public.alert_type_id_seq', (SELECT MAX(id) FROM public.alert_type));
  PERFORM import_from_csv('public.alert_history', folder_path);
  PERFORM setval('public.alert_history_id_seq', (SELECT MAX(id) FROM public.alert_history));
  PERFORM import_from_csv('public.alert_substitution_value', folder_path);
  PERFORM import_from_csv('public.alert_search_tag', folder_path);
  PERFORM setval('public.alert_search_tag_id_seq', (SELECT MAX(id) FROM public.alert_search_tag));
  PERFORM import_from_csv('public.alert_digest_history', folder_path);
  PERFORM import_from_csv('meta.tag_category', folder_path);
  PERFORM import_from_csv('meta.tag_type', folder_path);
  PERFORM import_from_csv('meta.fixed_tag', folder_path);
END;
$$;
ALTER FUNCTION public.import_tables_from_csv(folder_path text) OWNER TO postgres;


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;


CREATE TABLE membership.organization
(
  id integer NOT NULL,
  name character varying(50) NOT NULL,
  is_master boolean NOT NULL,
  CONSTRAINT organization_pkey PRIMARY KEY (id)
    , CONSTRAINT organization_name_key UNIQUE (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE membership.organization
  OWNER TO postgres;

CREATE SEQUENCE membership.organization_id_seq;
ALTER TABLE membership.organization_id_seq OWNER TO postgres;

ALTER TABLE ONLY membership.organization ALTER COLUMN id SET DEFAULT nextval('membership.organization_id_seq'::regclass);

CREATE TABLE membership.login
(
  id integer NOT NULL,
  login_name character varying(255) NOT NULL,
  display_name character varying(100) NOT NULL,
  password character varying(100) NOT NULL,
  email character varying(255),
  organization_id integer NOT NULL,
  CONSTRAINT login_pkey PRIMARY KEY (id)
  , CONSTRAINT login_organization_id_fkey FOREIGN KEY (organization_id)
      REFERENCES membership.organization (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
    , CONSTRAINT login_email_login_name_key UNIQUE (email, login_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE membership.login
  OWNER TO postgres;

CREATE SEQUENCE membership.login_id_seq;
ALTER TABLE membership.login_id_seq OWNER TO postgres;

ALTER TABLE ONLY membership.login ALTER COLUMN id SET DEFAULT nextval('membership.login_id_seq'::regclass);

CREATE TABLE membership.session
(
  id character varying(32) NOT NULL,
  login_id integer NOT NULL,
  last_activity_date timestamp without time zone NOT NULL,
  CONSTRAINT session_pkey PRIMARY KEY (id)
  , CONSTRAINT session_login_id_fkey FOREIGN KEY (login_id)
      REFERENCES membership.login (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE membership.session
  OWNER TO postgres;

CREATE TABLE public.data_provider
(
  id character varying(2) NOT NULL,
  name character varying(20) NOT NULL,
  CONSTRAINT data_provider_pkey PRIMARY KEY (id)
    , CONSTRAINT data_provider_name_key UNIQUE (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.data_provider
  OWNER TO postgres;

CREATE TABLE public.esg_rating
(
  data_provider_id character varying(2),
  id character varying(5),
  CONSTRAINT esg_rating_pkey PRIMARY KEY (data_provider_id, id)
  , CONSTRAINT esg_rating_data_provider_id_fkey FOREIGN KEY (data_provider_id)
      REFERENCES public.data_provider (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.esg_rating
  OWNER TO postgres;

CREATE TABLE public.esg_factor
(
  id integer NOT NULL,
  name character varying(50),
  data_provider_id character varying(2),
  level integer NOT NULL,
  parent_id integer,
  esg_type character varying(1),
  weight double precision,
  CONSTRAINT esg_factor_pkey PRIMARY KEY (id)
  , CONSTRAINT esg_factor_data_provider_id_fkey FOREIGN KEY (data_provider_id)
      REFERENCES public.data_provider (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT esg_factor_parent_id_fkey FOREIGN KEY (parent_id)
      REFERENCES public.esg_factor (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.esg_factor
  OWNER TO postgres;

CREATE TABLE public.weight_method
(
  id integer NOT NULL,
  name character varying(20),
  CONSTRAINT weight_method_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.weight_method
  OWNER TO postgres;

CREATE TABLE public.exchange_rate
(
  currency_id character varying(3),
  date_key date,
  adjusted_close_price double precision,
  usd_return_daily_log double precision,
  usd_return_log_cumulative_sum double precision,
  CONSTRAINT exchange_rate_pkey PRIMARY KEY (currency_id, date_key)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.exchange_rate
  OWNER TO postgres;

CREATE TABLE public.geography
(
  id integer NOT NULL,
  name character varying(200) NOT NULL,
  level integer NOT NULL,
  parent_id integer,
  code character varying(10),
  CONSTRAINT geography_pkey PRIMARY KEY (id)
  , CONSTRAINT geography_parent_id_fkey FOREIGN KEY (parent_id)
      REFERENCES public.geography (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.geography
  OWNER TO postgres;

CREATE TABLE public.sector
(
  id integer NOT NULL,
  name character varying(50) NOT NULL,
  level integer NOT NULL,
  parent_id integer,
  CONSTRAINT sector_pkey PRIMARY KEY (id)
  , CONSTRAINT sector_parent_id_fkey FOREIGN KEY (parent_id)
      REFERENCES public.sector (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.sector
  OWNER TO postgres;

CREATE TABLE public.correlation_group
(
  id integer NOT NULL,
  name character varying(50),
  r_squared double precision,
  asset_value double precision,
  asset_volatility double precision,
  current_liabilities double precision,
  long_term_debt double precision,
  total_debt double precision,
  market_cap double precision,
  CONSTRAINT correlation_group_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.correlation_group
  OWNER TO postgres;

CREATE SEQUENCE public.correlation_group_id_seq;
ALTER TABLE public.correlation_group_id_seq OWNER TO postgres;

ALTER TABLE ONLY public.correlation_group ALTER COLUMN id SET DEFAULT nextval('public.correlation_group_id_seq'::regclass);

CREATE TABLE public.asset_type
(
  id integer NOT NULL,
  name character varying(50) NOT NULL,
  level integer NOT NULL,
  parent_id integer,
  CONSTRAINT asset_type_pkey PRIMARY KEY (id)
  , CONSTRAINT asset_type_parent_id_fkey FOREIGN KEY (parent_id)
      REFERENCES public.asset_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
    , CONSTRAINT asset_type_name_key UNIQUE (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.asset_type
  OWNER TO postgres;

CREATE TABLE public.company
(
  id character varying(20) NOT NULL,
  ara_id character varying(15),
  name character varying(200) NOT NULL,
  geography_id integer NOT NULL,
  sector_id integer,
  CONSTRAINT company_pkey PRIMARY KEY (id)
  , CONSTRAINT company_geography_id_fkey FOREIGN KEY (geography_id)
      REFERENCES public.geography (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT company_sector_id_fkey FOREIGN KEY (sector_id)
      REFERENCES public.sector (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.company
  OWNER TO postgres;

CREATE TABLE public.company_esg_factor
(
  company_id character varying(20),
  esg_factor_id integer,
  date_key date,
  score double precision,
  CONSTRAINT company_esg_factor_pkey PRIMARY KEY (company_id, esg_factor_id, date_key)
  , CONSTRAINT company_esg_factor_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES public.company (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT company_esg_factor_esg_factor_id_fkey FOREIGN KEY (esg_factor_id)
      REFERENCES public.esg_factor (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.company_esg_factor
  OWNER TO postgres;

CREATE TABLE public.company_esg_summary
(
  company_id character varying(20),
  data_provider_id character varying(2),
  rating_id character varying(5),
  esg_score double precision,
  e_score double precision,
  s_score double precision,
  g_score double precision,
  revenue double precision,
  CONSTRAINT company_esg_summary_pkey PRIMARY KEY (company_id, data_provider_id)
  , CONSTRAINT company_esg_summary_data_provider_id_rating_id_fkey FOREIGN KEY (data_provider_id, rating_id)
      REFERENCES public.esg_rating (data_provider_id, id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT company_esg_summary_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES public.company (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT company_esg_summary_data_provider_id_fkey FOREIGN KEY (data_provider_id)
      REFERENCES public.data_provider (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.company_esg_summary
  OWNER TO postgres;

CREATE TABLE public.company_supplier
(
  company_id character varying(20),
  supplier_id character varying(20),
  create_date timestamp without time zone,
  CONSTRAINT company_supplier_pkey PRIMARY KEY (company_id, supplier_id)
  , CONSTRAINT company_supplier_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES public.company (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT company_supplier_supplier_id_fkey FOREIGN KEY (supplier_id)
      REFERENCES public.company (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.company_supplier
  OWNER TO postgres;

CREATE TABLE public.company_asset
(
  company_id character varying(20),
  asset_type_id integer,
  volume double precision,
  CONSTRAINT company_asset_pkey PRIMARY KEY (company_id, asset_type_id)
  , CONSTRAINT company_asset_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES public.company (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT company_asset_asset_type_id_fkey FOREIGN KEY (asset_type_id)
      REFERENCES public.asset_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.company_asset
  OWNER TO postgres;

CREATE TABLE public.security
(
  id character varying(20) NOT NULL,
  name character varying(200) NOT NULL,
  company_id character varying(20) NOT NULL,
  asset_type_id integer NOT NULL,
  isin character varying(12),
  sedol character varying(7),
  cusip character varying(9),
  CONSTRAINT security_pkey PRIMARY KEY (id)
  , CONSTRAINT security_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES public.company (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT security_asset_type_id_fkey FOREIGN KEY (asset_type_id)
      REFERENCES public.asset_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.security
  OWNER TO postgres;

CREATE TABLE public.company_primary_security
(
  company_id character varying(20),
  asset_type_id integer,
  security_id character varying(20),
  CONSTRAINT company_primary_security_pkey PRIMARY KEY (company_id, asset_type_id)
  , CONSTRAINT company_primary_security_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES public.company (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT company_primary_security_asset_type_id_fkey FOREIGN KEY (asset_type_id)
      REFERENCES public.asset_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT company_primary_security_security_id_fkey FOREIGN KEY (security_id)
      REFERENCES public.security (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.company_primary_security
  OWNER TO postgres;

CREATE TABLE public.security_financial_series
(
  security_id character varying(20),
  date_key date,
  sector_id integer,
  closing_price double precision,
  volume double precision,
  return_daily double precision,
  return_daily_log double precision,
  return_daily_cumulative double precision,
  return_daily_log_cumulative double precision,
  volatility double precision,
  sharpe_ratio double precision,
  vasicek_ratio double precision,
  mc_expected_loss_gross double precision,
  risk_contribution double precision,
  tail_risk_contribution  double precision,
  rorac double precision,
  CONSTRAINT security_financial_series_pkey PRIMARY KEY (security_id, date_key)
  , CONSTRAINT security_financial_series_security_id_fkey FOREIGN KEY (security_id)
      REFERENCES public.security (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT security_financial_series_sector_id_fkey FOREIGN KEY (sector_id)
      REFERENCES public.sector (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.security_financial_series
  OWNER TO postgres;

CREATE TABLE public.portfolio
(
  id integer NOT NULL,
  name character varying(200) NOT NULL,
  import_name character varying(200),
  as_of date NOT NULL,
  is_reference boolean NOT NULL,
  owner_id integer,
  create_date timestamp without time zone,
  CONSTRAINT portfolio_pkey PRIMARY KEY (id)
  , CONSTRAINT portfolio_owner_id_fkey FOREIGN KEY (owner_id)
      REFERENCES membership.organization (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
    , CONSTRAINT portfolio_name_key UNIQUE (name)
    , CONSTRAINT portfolio_import_name_key UNIQUE (import_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.portfolio
  OWNER TO postgres;

CREATE SEQUENCE public.portfolio_id_seq;
ALTER TABLE public.portfolio_id_seq OWNER TO postgres;

ALTER TABLE ONLY public.portfolio ALTER COLUMN id SET DEFAULT nextval('public.portfolio_id_seq'::regclass);

CREATE TABLE public.portfolio_security
(
  portfolio_id integer NOT NULL,
  security_id character varying(20) NOT NULL,
  portfolio_update_date date NOT NULL,
  position double precision NOT NULL,
  CONSTRAINT portfolio_security_pkey PRIMARY KEY (portfolio_id, security_id, portfolio_update_date)
  , CONSTRAINT portfolio_security_portfolio_id_fkey FOREIGN KEY (portfolio_id)
      REFERENCES public.portfolio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT portfolio_security_security_id_fkey FOREIGN KEY (security_id)
      REFERENCES public.security (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.portfolio_security
  OWNER TO postgres;

CREATE TABLE public.portfolio_security_value
(
  portfolio_id integer NOT NULL,
  security_id character varying(20) NOT NULL,
  date_key date NOT NULL,
  weight double precision,
  base_currency_value double precision,
  CONSTRAINT portfolio_security_value_pkey PRIMARY KEY (portfolio_id, security_id, date_key)
  , CONSTRAINT portfolio_security_value_portfolio_id_fkey FOREIGN KEY (portfolio_id)
      REFERENCES public.portfolio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT portfolio_security_value_security_id_fkey FOREIGN KEY (security_id)
      REFERENCES public.security (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.portfolio_security_value
  OWNER TO postgres;

CREATE TABLE public.portfolio_result
(
  portfolio_id integer NOT NULL,
  date_key date NOT NULL,
  number_securities integer,
  market_value double precision,
  return_daily double precision,
  cumulative_return double precision,
  volatility double precision,
  sharpe_ratio double precision,
  var_3_pct double precision,
  etl_3_pct double precision,
  expected_loss double precision,
  vasicek_ratio_3_pct double precision,
  CONSTRAINT portfolio_result_pkey PRIMARY KEY (portfolio_id, date_key)
  , CONSTRAINT portfolio_result_portfolio_id_fkey FOREIGN KEY (portfolio_id)
      REFERENCES public.portfolio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.portfolio_result
  OWNER TO postgres;

CREATE TABLE public.portfolio_esg_score
(
  portfolio_id integer NOT NULL,
  date_key date NOT NULL,
  esg_factor_id integer,
  weight_method integer,
  score double precision,
  CONSTRAINT portfolio_esg_score_pkey PRIMARY KEY (portfolio_id, date_key, esg_factor_id, weight_method)
  , CONSTRAINT portfolio_esg_score_portfolio_id_fkey FOREIGN KEY (portfolio_id)
      REFERENCES public.portfolio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT portfolio_esg_score_esg_factor_id_fkey FOREIGN KEY (esg_factor_id)
      REFERENCES public.esg_factor (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT portfolio_esg_score_weight_method_fkey FOREIGN KEY (weight_method)
      REFERENCES public.weight_method (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.portfolio_esg_score
  OWNER TO postgres;

CREATE TABLE public.grouping
(
  id integer NOT NULL,
  name character varying(100) NOT NULL,
  sector_id integer,
  geography_id integer,
  esg_factor_id integer,
  analysis character varying(32),
  CONSTRAINT grouping_pkey PRIMARY KEY (id)
  , CONSTRAINT grouping_sector_id_fkey FOREIGN KEY (sector_id)
      REFERENCES public.sector (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT grouping_geography_id_fkey FOREIGN KEY (geography_id)
      REFERENCES public.geography (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT grouping_esg_factor_id_fkey FOREIGN KEY (esg_factor_id)
      REFERENCES public.esg_factor (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.grouping
  OWNER TO postgres;

CREATE TABLE public.metric
(
  id integer NOT NULL,
  name character varying(50) NOT NULL,
  provider character varying(20) NOT NULL,
  CONSTRAINT metric_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.metric
  OWNER TO postgres;

CREATE TABLE public.portfolio_metric_date
(
  id integer NOT NULL,
  portfolio_id integer NOT NULL,
  date_key date NOT NULL,
  CONSTRAINT portfolio_metric_date_pkey PRIMARY KEY (id)
  , CONSTRAINT portfolio_metric_date_portfolio_id_fkey FOREIGN KEY (portfolio_id)
      REFERENCES public.portfolio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
    , CONSTRAINT portfolio_metric_date_portfolio_id_date_key_key UNIQUE (portfolio_id, date_key)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.portfolio_metric_date
  OWNER TO postgres;

CREATE SEQUENCE public.portfolio_metric_date_id_seq;
ALTER TABLE public.portfolio_metric_date_id_seq OWNER TO postgres;

ALTER TABLE ONLY public.portfolio_metric_date ALTER COLUMN id SET DEFAULT nextval('public.portfolio_metric_date_id_seq'::regclass);

CREATE TABLE public.portfolio_grouping_metric
(
  portfolio_metric_date_id integer NOT NULL,
  metric_id integer NOT NULL,
  grouping_id integer NOT NULL,
  value double precision,
  CONSTRAINT portfolio_grouping_metric_pkey PRIMARY KEY (portfolio_metric_date_id, metric_id, grouping_id)
  , CONSTRAINT portfolio_grouping_metric_portfolio_metric_date_id_fkey FOREIGN KEY (portfolio_metric_date_id)
      REFERENCES public.portfolio_metric_date (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT portfolio_grouping_metric_metric_id_fkey FOREIGN KEY (metric_id)
      REFERENCES public.metric (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT portfolio_grouping_metric_grouping_id_fkey FOREIGN KEY (grouping_id)
      REFERENCES public.grouping (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.portfolio_grouping_metric
  OWNER TO postgres;

CREATE TABLE public.security_esg_factor
(
  portfolio_id integer NOT NULL,
  security_id character varying(20) NOT NULL,
  date_key date NOT NULL,
  esg_factor_id integer NOT NULL,
  metric_id integer NOT NULL,
  grouping_id integer NOT NULL,
  value double precision,
  CONSTRAINT security_esg_factor_pkey PRIMARY KEY (portfolio_id, security_id, date_key, esg_factor_id, metric_id, grouping_id)
  , CONSTRAINT security_esg_factor_portfolio_id_fkey FOREIGN KEY (portfolio_id)
      REFERENCES public.portfolio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT security_esg_factor_security_id_fkey FOREIGN KEY (security_id)
      REFERENCES public.security (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT security_esg_factor_esg_factor_id_fkey FOREIGN KEY (esg_factor_id)
      REFERENCES public.esg_factor (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT security_esg_factor_metric_id_fkey FOREIGN KEY (metric_id)
      REFERENCES public.metric (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT security_esg_factor_grouping_id_fkey FOREIGN KEY (grouping_id)
      REFERENCES public.grouping (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.security_esg_factor
  OWNER TO postgres;

CREATE TABLE public.tag_history
(
  id integer NOT NULL,
  name character varying(100) NOT NULL,
  tag_combination json NOT NULL,
  create_date date,
  owner_id integer,
  CONSTRAINT tag_history_pkey PRIMARY KEY (id)
    , CONSTRAINT tag_history_name_key UNIQUE (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.tag_history
  OWNER TO postgres;

CREATE SEQUENCE public.tag_history_id_seq;
ALTER TABLE public.tag_history_id_seq OWNER TO postgres;

ALTER TABLE ONLY public.tag_history ALTER COLUMN id SET DEFAULT nextval('public.tag_history_id_seq'::regclass);

CREATE TABLE public.alert_type
(
  id integer NOT NULL,
  name character varying(50) NOT NULL,
  text_template character varying(1000) NOT NULL,
  target character varying(1) NOT NULL,
  CONSTRAINT alert_type_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.alert_type
  OWNER TO postgres;

CREATE SEQUENCE public.alert_type_id_seq;
ALTER TABLE public.alert_type_id_seq OWNER TO postgres;

ALTER TABLE ONLY public.alert_type ALTER COLUMN id SET DEFAULT nextval('public.alert_type_id_seq'::regclass);

CREATE TABLE public.alert_history
(
  id integer NOT NULL,
  alert_type_id integer NOT NULL,
  date_key date NOT NULL,
  portfolio_id integer,
  portfolio_name character varying(200),
  company_id character varying(20),
  company_name character varying(200),
  data_provider_id character varying(2),
  data_provider_name character varying(20),
  esg_factor_id integer,
  esg_factor_name character varying(50),
  region_id integer,
  region_name character varying(200),
  country_id integer,
  country_name character varying(200),
  sector_id integer,
  sector_name character varying(50),
  industry_id integer,
  industry_name character varying(50),
  CONSTRAINT alert_history_pkey PRIMARY KEY (id)
  , CONSTRAINT alert_history_alert_type_id_fkey FOREIGN KEY (alert_type_id)
      REFERENCES public.alert_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT alert_history_portfolio_id_fkey FOREIGN KEY (portfolio_id)
      REFERENCES public.portfolio (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT alert_history_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES public.company (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT alert_history_data_provider_id_fkey FOREIGN KEY (data_provider_id)
      REFERENCES public.data_provider (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT alert_history_esg_factor_id_fkey FOREIGN KEY (esg_factor_id)
      REFERENCES public.esg_factor (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT alert_history_region_id_fkey FOREIGN KEY (region_id)
      REFERENCES public.geography (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT alert_history_country_id_fkey FOREIGN KEY (country_id)
      REFERENCES public.geography (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT alert_history_sector_id_fkey FOREIGN KEY (sector_id)
      REFERENCES public.sector (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT alert_history_industry_id_fkey FOREIGN KEY (industry_id)
      REFERENCES public.sector (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.alert_history
  OWNER TO postgres;

CREATE SEQUENCE public.alert_history_id_seq;
ALTER TABLE public.alert_history_id_seq OWNER TO postgres;

ALTER TABLE ONLY public.alert_history ALTER COLUMN id SET DEFAULT nextval('public.alert_history_id_seq'::regclass);

CREATE TABLE public.alert_substitution_value
(
  alert_history_id integer NOT NULL,
  index integer NOT NULL,
  value character varying(100),
  CONSTRAINT alert_substitution_value_pkey PRIMARY KEY (alert_history_id, index)
  , CONSTRAINT alert_substitution_value_alert_history_id_fkey FOREIGN KEY (alert_history_id)
      REFERENCES public.alert_history (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.alert_substitution_value
  OWNER TO postgres;

CREATE TABLE public.alert_search_tag
(
  id integer NOT NULL,
  alert_type_id integer NOT NULL,
  tag_type_id integer NOT NULL,
  tag_id integer,
  tag_name character varying(50),
  level integer,
  CONSTRAINT alert_search_tag_pkey PRIMARY KEY (id)
  , CONSTRAINT alert_search_tag_alert_type_id_fkey FOREIGN KEY (alert_type_id)
      REFERENCES public.alert_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.alert_search_tag
  OWNER TO postgres;

CREATE SEQUENCE public.alert_search_tag_id_seq;
ALTER TABLE public.alert_search_tag_id_seq OWNER TO postgres;

ALTER TABLE ONLY public.alert_search_tag ALTER COLUMN id SET DEFAULT nextval('public.alert_search_tag_id_seq'::regclass);

CREATE TABLE public.alert_digest_history
(
  alert_history_id integer NOT NULL,
  login_id integer NOT NULL,
  is_dismissed boolean NOT NULL,
  CONSTRAINT alert_digest_history_pkey PRIMARY KEY (alert_history_id, login_id)
  , CONSTRAINT alert_digest_history_alert_history_id_fkey FOREIGN KEY (alert_history_id)
      REFERENCES public.alert_history (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
  , CONSTRAINT alert_digest_history_login_id_fkey FOREIGN KEY (login_id)
      REFERENCES membership.login (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.alert_digest_history
  OWNER TO postgres;

CREATE TABLE meta.tag_category
(
  id integer NOT NULL,
  description character varying(20) NOT NULL,
  CONSTRAINT tag_category_pkey PRIMARY KEY (id)
    , CONSTRAINT tag_category_description_key UNIQUE (description)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE meta.tag_category
  OWNER TO postgres;

CREATE TABLE meta.tag_type
(
  id integer NOT NULL,
  description character varying(30) NOT NULL,
  tag_category_id integer NOT NULL,
  is_from_table_data boolean NOT NULL,
  CONSTRAINT tag_type_pkey PRIMARY KEY (id)
  , CONSTRAINT tag_type_tag_category_id_fkey FOREIGN KEY (tag_category_id)
      REFERENCES meta.tag_category (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE meta.tag_type
  OWNER TO postgres;

CREATE TABLE meta.fixed_tag
(
  id integer NOT NULL,
  tag_type_id integer NOT NULL,
  description character varying(30) NOT NULL,
  table_name character varying(30),
  field_name character varying(30),
  CONSTRAINT fixed_tag_pkey PRIMARY KEY (id)
  , CONSTRAINT fixed_tag_tag_type_id_fkey FOREIGN KEY (tag_type_id)
      REFERENCES meta.tag_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE meta.fixed_tag
  OWNER TO postgres;


CREATE EXTENSION file_fdw;
CREATE SERVER import_esg FOREIGN DATA WRAPPER file_fdw;

-------------------------------------------------------------------------------------------------------
-- Step 3: Create functions
-------------------------------------------------------------------------------------------------------

SET search_path = membership;

create or replace function hash_password(p_password text)
returns text
as $$
    SELECT membership.crypt(p_password, membership.gen_salt('bf', 10)) 
$$
language sql;


drop function if exists membership.logoff(varchar);

create function membership.logoff(p_session_id varchar)
returns void as
$$
    delete from membership.session where id = p_session_id;
$$ LANGUAGE SQL;


create or replace function logon(p_login_name varchar, p_password varchar)
returns TABLE (
    success boolean,
    login_id int,
    session_id varchar(32)
) as
$$
DECLARE
    v_login_id int;
    v_success boolean;
    v_session_id varchar(32);
BEGIN

    select False into v_success;

    -- crypt() will return different values each time it's called, but crypt(value1, value2) will check if values match
    select id from membership.login where membership.login.login_name = p_login_name and membership.crypt(p_password, password) = password into v_login_id;
    
    if v_login_id is not NULL then
        select membership.random_string() into v_session_id;
        
        insert into membership.session (id, login_id, last_activity_date) values (v_session_id, v_login_id, now());

        select True into v_success;
    end if;

    return query
    select v_success, v_login_id, v_session_id;
END;
$$ LANGUAGE PLPGSQL;



create or replace function random_string(p_len int default 32)
returns text
as $$
    select substring(md5(random()::text), 0, p_len + 1);
$$
language sql;


drop function if exists membership.validate_session(varchar);

create function membership.validate_session(p_session_id varchar)
returns table(
    is_active boolean,
    organization_id int,
    is_master boolean,
    login_id int
) as
$$
DECLARE
    v_is_active boolean;
    v_org_id int;
    v_is_master boolean;
    v_login_id int;
BEGIN
    -- Set defaults
    select False, NULL, False, NULL into v_is_active, v_org_id, v_is_master, v_login_id;
    
    select True, o.id, o.is_master, l.id into v_is_active, v_org_id, v_is_master, v_login_id
    from membership.session s join membership.login l on s.login_id = l.id join membership.organization o on l.organization_id = o.id
    where s.id = p_session_id and s.last_activity_date between (now() - INTERVAL '15 minutes') and now();

    update membership.session set last_activity_date = now() where id = p_session_id;
    
    return query
    select v_is_active, v_org_id, v_is_master, v_login_id;
END;
$$ LANGUAGE PLPGSQL;



SET search_path = public, pg_catalog;

create or replace function alert_dismiss(p_alert_history_id int, p_login_id int)
returns void as
$$
DECLARE
    v_alert_history_id int;
BEGIN

    select alert_history_id from alert_digest_history where alert_history_id = p_alert_history_id and login_id = p_login_id into v_alert_history_id;
    
    if v_alert_history_id is NULL then
        insert into alert_digest_history (alert_history_id, login_id, is_dismissed) values (p_alert_history_id, p_login_id, True);
    else
        update alert_digest_history set is_dismissed = True where alert_history_id = p_alert_history_id and login_id = p_login_id;
    end if;

END;
$$ LANGUAGE PLPGSQL;



create or replace function alert_dismiss_all(p_login_id int)
returns void as
$$
BEGIN

    update alert_digest_history set is_dismissed = True where login_id = p_login_id;
    
    insert into alert_digest_history (alert_history_id, login_id, is_dismissed)
    select distinct alert_history_id, p_login_id, True 
    from get_alert_history(p_login_id) h where h.alert_history_id not in (select alert_history_id from alert_digest_history where login_id = p_login_id);

END;
$$ LANGUAGE PLPGSQL;



create or replace function alert_mark_all_read(p_login_id int)
returns void as
$$
BEGIN

    insert into alert_digest_history (alert_history_id, login_id, is_dismissed)
    select distinct alert_history_id, p_login_id, False 
    from get_alert_history(p_login_id) h where h.alert_history_id not in (select alert_history_id from alert_digest_history where login_id = p_login_id);

END;
$$ LANGUAGE plpgsql;


create or replace function alert_mark_read(p_alert_history_id int, p_login_id int)
returns void as
$$
DECLARE
    v_alert_history_id int;
BEGIN

    select alert_history_id from alert_digest_history where alert_history_id = p_alert_history_id and login_id = p_login_id into v_alert_history_id;
    
    if v_alert_history_id is NULL then
        insert into alert_digest_history (alert_history_id, login_id, is_dismissed) values (p_alert_history_id, p_login_id, False);
    end if;

END;
$$ LANGUAGE PLPGSQL;



drop function if exists get_alert_history(int);

create or replace function get_alert_history(p_login_id int)
returns table(
    alert_history_id int,
    date_key date,
    data_provider_id varchar,
    data_provider_name varchar,
    company_id varchar,
    company_name varchar,
	text_template varchar,
	target varchar,
	index int,
	value varchar,
	is_new bool
)
as $$

    select 
        h.id,
        h.date_key,
        h.data_provider_id,
        h.data_provider_name,
        h.company_id,
        h.company_name,
        t.text_template,
        t.target,
        v.index,
        v.value,
        d.alert_history_id IS NULL as is_new
    from
        membership.login l
        join membership.organization o on l.organization_id = o.id
        join portfolio p on p.owner_id IS NULL or p.owner_id = l.organization_id or o.is_master
        join alert_history h on p.id = h.portfolio_id
        join alert_type t on h.alert_type_id = t.id
        join alert_substitution_value v on v.alert_history_id = h.id
        left join alert_digest_history d on h.id = d.alert_history_id and l.id = d.login_id
    where
        l.id = p_login_id and COALESCE(d.is_dismissed, False) = False
    order by
        h.id, v.index;

$$
LANGUAGE SQL;


drop function if exists get_alert_search_tags();

create or replace function get_alert_search_tags()
returns table (
    alert_history_id int,
    date_key date,
    portfolio_id int,
    portfolio_name varchar,
    esg_factor_id int,
    esg_factor_name varchar,
    region_id int,
    region_name varchar,
    country_id int,
    country_name varchar,
    sector_id int,
    sector_name varchar,
    industry_id int,
    industry_name varchar,
    tag_type_id int,
    tag_id int, 
    tag_name varchar, 
    level int
)
as $$

    select
        h.id,
        h.date_key,
        h.portfolio_id,
        h.portfolio_name,
        h.esg_factor_id,
        h.esg_factor_name,
        h.region_id,
        h.region_name,
        h.country_id,
        h.country_name,
        h.sector_id,
        h.sector_name,
        h.industry_id,
        h.industry_name,
        s.tag_type_id,
        s.tag_id, 
        s.tag_name, 
        s.level
    from
        alert_history h join alert_search_tag s on s.alert_type_id = h.alert_type_id
    order by
        h.id,
        s.id
        
$$
LANGUAGE SQL;


create or replace function get_company_esg_factor_percentages(p_company_id varchar, p_data_provider_id varchar, p_date_key date)
returns table(
	factor_id integer,
	factor_name varchar(50),
	esg_type char(1),
	level integer,
	parent_id integer,
	score float,
	group_percentage float,
	weighted_score float,
	weighted_percentage float
)
as $$

	with
	    -- Calculate weighted and unweighted scores for each factor and percentage of parent
	    scores_by_factor as (
            select f.id as factor_id, f.name, f.esg_type, f.parent_id, f.level, c.company_id, f.data_provider_id, c.date_key, c.score, 
                abs(c.score) / sum(abs(c.score)) over (partition by company_id, data_provider_id, date_key, parent_id) as unweighted_percent_of_parent,
                f.weight, c.score * f.weight as weighted_score, 
                abs(c.score * f.weight) / sum(abs(c.score * f.weight)) over (partition by company_id, data_provider_id, date_key, parent_id) as weighted_percent_of_parent
            from company_esg_factor c join esg_factor f on c.esg_factor_id = f.id
            where company_id = p_company_id and data_provider_id = p_data_provider_id and date_key = p_date_key
	    ),
	    scaled_by_parent as (
            select s.*, COALESCE(p.unweighted_percent_of_parent, 1) as unweighted_parent_scaling, s.unweighted_percent_of_parent * COALESCE(p.unweighted_percent_of_parent, 1) as unweighted_scaled_to_parent, 
                COALESCE(p.weighted_percent_of_parent, 1) as weighted_parent_scaling, s.weighted_percent_of_parent * COALESCE(p.weighted_percent_of_parent, 1) as weighted_scaled_to_parent
            from scores_by_factor s 
                left outer join scores_by_factor p on s.parent_id = p.factor_id
	    ),
	    fully_scaled as (
            select s.*, s.unweighted_percent_of_parent * COALESCE(p.unweighted_scaled_to_parent, 1) as unweighted_percentage, s.weighted_percent_of_parent * COALESCE(p.weighted_scaled_to_parent, 1) as weighted_percentage
            from scaled_by_parent s 
                left outer join scaled_by_parent p on s.parent_id = p.factor_id
	    )
	select factor_id, name, esg_type, level, parent_id, score, unweighted_percentage, weighted_score, weighted_percentage
	from fully_scaled
	order by level, factor_id
	
$$
LANGUAGE SQL;


create or replace function get_company_esg_factor_percentages(p_company_id varchar, p_data_provider_id varchar)
returns table(
	factor_id integer,
	factor_name varchar(50),
	esg_type char(1),
	level integer,
	parent_id integer,
	score float,
	group_percentage float,
	weighted_score float,
	weighted_percentage float
)
as $$

	select get_company_esg_factor_percentages(p_company_id, p_data_provider_id, max(date_key))
	from company_esg_factor c join esg_factor f on c.esg_factor_id = f.id
	where f.data_provider_id = p_data_provider_id and company_id = p_company_id
	group by c.company_id
	
$$
LANGUAGE SQL;


create or replace function get_esg_summary_series(p_company_id varchar, p_data_provider_id varchar)
returns table(
	date_key date,
	factor_id int,
	score float
)
as $$

	select cf.date_key, f.id, cf.score
	from company_esg_factor cf join esg_factor f on cf.esg_factor_id = f.id
	where cf.company_id = p_company_id and f.data_provider_id = p_data_provider_id and f.level <= 2
	order by cf.date_key, f.level, f.id
	
$$
LANGUAGE SQL;


create or replace function import_data(p_import_folder text, p_start_date date DEFAULT null)
returns void
as $$
BEGIN

	EXECUTE format('
		CREATE FOREIGN TABLE import_company
		(
		  company_id character varying(20) NOT NULL,
		  ara_id character varying(15),
		  name character varying(200) NOT NULL,
		  geography_id integer NOT NULL,
		  sector_id integer
		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/company.csv');

	insert into company(id, ara_id, name, geography_id, sector_id)
	select company_id, ara_id, name, geography_id, sector_id from import_company
	on conflict (id) do update
	  set
	    ara_id = EXCLUDED.ara_id,
	    name = EXCLUDED.name,
	    geography_id = EXCLUDED.geography_id,
	    sector_id = EXCLUDED.sector_id;

	EXECUTE format('
		CREATE FOREIGN TABLE import_security 
		(
		  security_id character varying(20) NOT NULL,
		  name character varying(200) NOT NULL,
		  company_id character varying(50) NOT NULL,
		  asset_type_id integer NOT NULL,
		  isin character varying(12),
		  sedol character varying(7),
		  cusip character varying(9)
		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/security.csv');

	insert into security (id, name, company_id, asset_type_id, isin, sedol, cusip)
	select security_id, name, company_id, asset_type_id, isin, sedol, cusip 
	from import_security
	on conflict (id)
	DO UPDATE
	  SET 
	    name = EXCLUDED.name,
	    isin = EXCLUDED.isin,
	    sedol = EXCLUDED.sedol,
	    cusip = EXCLUDED.cusip;

    --TODO: Change to populate a csv file containing correct data
    insert into company_primary_security (company_id, asset_type_id, security_id)
    select company_id, 1, security_id
    from import_security
    on conflict (company_id, asset_type_id) do nothing;
    
	EXECUTE format('
		CREATE FOREIGN TABLE import_security_financial_series
		(
          security_id character varying(20) NOT NULL,
          date_key date NOT NULL,
          sector_id integer,
          closing_price double precision,
          volume double precision
		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/security_financial_series.csv');

	if p_start_date is not null then
		DELETE FROM security_financial_series WHERE date_key >= p_start_date and security_id in (
			select ps.security_id
			from portfolio_security ps
				join portfolio p on ps.portfolio_id = p.id
				join import_portfolio ip on p.import_name = ip.portfolio_name
		);
	end if;

	insert into security_financial_series (security_id, date_key, sector_id, closing_price, volume)
	select security_id, date_key, sector_id, closing_price, volume
	from import_security_financial_series
	on conflict (security_id, date_key)
	DO UPDATE
	  SET 
        sector_id = EXCLUDED.sector_id,
        closing_price = EXCLUDED.closing_price,
        volume = EXCLUDED.volume;

    /*
	EXECUTE format('
		CREATE FOREIGN TABLE import_exchange_rate
		(
          currency_id character varying(3) NOT NULL,
          date_key date NOT NULL,
          adjusted_close_price double precision,
          usd_return_daily_log double precision,
          usd_return_log_cumulative_sum double precision
  		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/exchange_rate.csv');

	if p_start_date is not null then
		DELETE FROM exchange_rate WHERE date_key >= p_start_date;
	end if;
	
	insert into exchange_rate (currency_id, date_key, adjusted_close_price, usd_return_daily_log, usd_return_log_cumulative_sum)
	select currency_id, date_key, adjusted_close_price, usd_return_daily_log, usd_return_log_cumulative_sum from import_exchange_rate
	on conflict on constraint exchange_rate_pkey
	DO UPDATE
	  SET 
	    adjusted_close_price = EXCLUDED.adjusted_close_price,
	    usd_return_daily_log = EXCLUDED.usd_return_daily_log,
	    usd_return_log_cumulative_sum = EXCLUDED.usd_return_log_cumulative_sum;
    */
    
	EXECUTE format('
		CREATE FOREIGN TABLE import_portfolio 
		(
		  portfolio_name character varying(200) NOT NULL,
		  as_of date NOT NULL,
		  is_reference boolean NOT NULL,
		  owner_id int
		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/portfolio.csv');

	insert into portfolio(name, import_name, as_of, is_reference, owner_id, create_date)
	select portfolio_name, portfolio_name, as_of, is_reference, owner_id, now()
	from import_portfolio
	on conflict on constraint portfolio_name_key DO NOTHING;

	EXECUTE format('
		CREATE FOREIGN TABLE import_portfolio_esg_score
		(
		  portfolio_name character varying(200) NOT NULL,
		  date_key date NOT NULL,
		  esg_factor_id integer NOT NULL,
		  weight_method integer NOT NULL,
		  score double precision
		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/portfolio_esg_score.csv');

	if p_start_date is not null then
		DELETE FROM portfolio_esg_score WHERE date_key >= p_start_date and portfolio_id in (
			select p.id from portfolio p join import_portfolio ip on p.import_name = ip.portfolio_name
		);
	end if;

	insert into portfolio_esg_score(portfolio_id, date_key, esg_factor_id, weight_method, score)
	select p.id, ie.date_key, ie.esg_factor_id, ie.weight_method, ie.score
	from import_portfolio_esg_score ie join portfolio p on ie.portfolio_name = p.import_name
	on conflict (portfolio_id, date_key, esg_factor_id, weight_method) 
	DO UPDATE SET
	  score = EXCLUDED.score;

	EXECUTE format('
		CREATE FOREIGN TABLE import_portfolio_result
		(
		  portfolio_name character varying(200) NOT NULL,
		  date_key date NOT NULL,
		  number_securities integer,
		  market_value double precision,
		  return_daily double precision,
		  cumulative_return double precision
  		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/portfolio_result.csv');

	if p_start_date is not null then
		DELETE FROM portfolio_result WHERE date_key >= p_start_date and portfolio_id in (
			select p.id from portfolio p join import_portfolio ip on p.import_name = ip.portfolio_name
		);
	end if;

	insert into portfolio_result(portfolio_id, date_key, number_securities, market_value, return_daily, cumulative_return)
	select p.id, ir.date_key, ir.number_securities, ir.market_value, ir.return_daily, ir.cumulative_return
	from import_portfolio_result ir join portfolio p on ir.portfolio_name = p.import_name
	on conflict (portfolio_id, date_key)
	DO UPDATE SET
	  number_securities = EXCLUDED.number_securities,
	  market_value = EXCLUDED.market_value,
	  return_daily = EXCLUDED.return_daily,
	  cumulative_return = EXCLUDED.cumulative_return;

	EXECUTE format('
		CREATE FOREIGN TABLE import_portfolio_security
		(
		  portfolio_name character varying(200) NOT NULL,
		  security_id character varying(20) NOT NULL,
		  portfolio_update_date date NOT NULL,
		  "position" double precision NOT NULL
  		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/portfolio_security.csv');

	if p_start_date is not null then
		DELETE FROM portfolio_security WHERE portfolio_update_date >= p_start_date and portfolio_id in (
			select p.id from portfolio p join import_portfolio ip on p.import_name = ip.portfolio_name
		);
	end if;

	insert into portfolio_security(portfolio_id, security_id, portfolio_update_date, "position")
	select p.id, ips.security_id, ips.portfolio_update_date, "position"
	from import_portfolio_security ips join portfolio p on ips.portfolio_name = p.import_name
	on conflict (portfolio_id, security_id, portfolio_update_date)
	DO UPDATE SET
	  "position" = EXCLUDED."position";

	EXECUTE format('
		CREATE FOREIGN TABLE import_portfolio_security_value
		(
		  portfolio_name character varying(200) NOT NULL,
		  security_id character varying(20) NOT NULL,
		  date_key date NOT NULL,
		  weight double precision,
		  base_currency_value double precision
  		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/portfolio_security_value.csv');

	if p_start_date is not null then
		DELETE FROM portfolio_security_value WHERE date_key >= p_start_date and portfolio_id in (
			select p.id from portfolio p join import_portfolio ip on p.import_name = ip.portfolio_name
		);
	end if;

	insert into portfolio_security_value(portfolio_id, security_id, date_key, weight, base_currency_value)
	select p.id, iv.security_id, iv.date_key, iv.weight, iv.base_currency_value
	from import_portfolio_security_value iv join portfolio p on iv.portfolio_name = p.import_name
	on conflict (portfolio_id, security_id, date_key)
	DO UPDATE SET
	  weight = EXCLUDED.weight,
	  base_currency_value = EXCLUDED.base_currency_value;

	EXECUTE format('
		CREATE FOREIGN TABLE import_portfolio_grouping_metric
		(
		  portfolio_name character varying(200) NOT NULL,
		  date_key date NOT NULL,
		  metric_id integer NOT NULL,
		  grouping_id integer NOT NULL,
		  value double precision
  		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/portfolio_grouping_metric.csv');

	if p_start_date is not null then
		DELETE FROM portfolio_grouping_metric WHERE portfolio_metric_date_id in (
			select d.id from portfolio_metric_date d join portfolio p on d.portfolio_id = p.id
			join import_portfolio ip on p.import_name = ip.portfolio_name
			where d.date_key >= p_start_date
		);

		DELETE FROM portfolio_metric_date WHERE date_key >= p_start_date and portfolio_id in (
			select p.id from portfolio p join import_portfolio ip on p.import_name = ip.portfolio_name
		);
	end if;

	insert into portfolio_metric_date(portfolio_id, date_key)
	select DISTINCT p.id, ig.date_key
	from import_portfolio_grouping_metric ig join portfolio p on ig.portfolio_name = p.import_name
	on conflict (portfolio_id, date_key) 
	DO NOTHING;

	insert into portfolio_grouping_metric(portfolio_metric_date_id, metric_id, grouping_id, value)
	select d.id, ig.metric_id, ig.grouping_id, ig.value
	from import_portfolio_grouping_metric ig join portfolio p on ig.portfolio_name = p.import_name
        join portfolio_metric_date d on p.id = d.portfolio_id and ig.date_key = d.date_key
	on conflict (portfolio_metric_date_id, metric_id, grouping_id) 
	DO UPDATE SET
	  value = EXCLUDED.value;
	    
    -- Save biggest table for last
	EXECUTE format('
		CREATE FOREIGN TABLE import_company_esg_factor
		(
		  company_id character varying(20) NOT NULL,
		  esg_factor_id integer NOT NULL,
		  date_key date NOT NULL,
		  score double precision
		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/company_esg_factor.csv');

	if p_start_date is not null then
		DELETE FROM company_esg_factor WHERE date_key >= p_start_date and company_id in (
			select c.id 
			from company c join security s on c.id = s.company_id 
				join portfolio_security ps on s.id = ps.security_id 
				join portfolio p on ps.portfolio_id = p.id
				join import_portfolio ip on p.import_name = ip.portfolio_name
		);
	end if;

	insert into company_esg_factor(company_id, esg_factor_id, date_key, score)
	select company_id, esg_factor_id, date_key, score from import_company_esg_factor
	on conflict (company_id, esg_factor_id, date_key) do update
	  set
	    score = EXCLUDED.score;

	EXECUTE format('
		CREATE FOREIGN TABLE import_alert_history 
		(
		  alert_history_id integer NOT NULL,
		  alert_type_id integer NOT NULL,
		  date_key date NOT NULL,
		  portfolio_id character varying(128) NOT NULL,
		  company_id character varying(32) NOT NULL,
		  company_name character varying(20) NOT NULL,
		  esg_factor_id integer NOT NULL,
		  region_id integer NOT NULL,
		  region_name character varying(64) NOT NULL,
		  country_id integer NOT NULL,
		  country_name character varying(64) NOT NULL,
		  sector_id integer NOT NULL,
		  sector_name character varying(64) NOT NULL,
		  industry_id integer NOT NULL,
		  industry_name character varying(64) NOT NULL
		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/alert_history.csv');

	if p_start_date is not null then

		DELETE FROM alert_history WHERE date_key >= p_start_date;

	end if;

	insert into alert_history (id, alert_type_id, date_key, portfolio_id, portfolio_name, company_id, company_name,
								data_provider_id, data_provider_name, esg_factor_id, esg_factor_name, region_id,
								region_name, country_id, country_name, sector_id, sector_name, industry_id, industry_name)
	select iah.alert_history_id, iah.alert_type_id, iah.date_key, p.id, p.name, iah.company_id, 
								iah.company_name,dp.id, dp.name, ef.id, ef.name, 
								iah.region_id,iah.region_name,iah.country_id, iah.country_name, 
								iah.sector_id, iah.sector_name, iah.industry_id, iah.industry_name
	from import_alert_history iah
	join esg_factor ef on iah.esg_factor_id = ef.id
	join data_provider dp on ef.data_provider_id = dp.id
	join portfolio p on iah.portfolio_id = p.import_name;

	EXECUTE format('
		CREATE FOREIGN TABLE import_alert_substitution_value 
		(
		  alert_history_id integer NOT NULL,
		  index integer NOT NULL,
		  value character varying(128) NOT NULL
		) SERVER import_esg
		OPTIONS ( filename %L, format ''csv'', header ''true'');', p_import_folder || '/alert_substitution_value.csv');

	if p_start_date is not null then

		DELETE FROM alert_substitution_value WHERE alert_history_id in (
			select id from alert_history WHERE date_key >= p_start_date
		);

	end if;

	insert into alert_substitution_value(alert_history_id, index,value)
	select alert_history_id, index, value from import_alert_substitution_value;

	DROP FOREIGN table import_portfolio_grouping_metric;
	DROP FOREIGN table import_portfolio_security_value;
	DROP FOREIGN table import_portfolio_security;
	DROP FOREIGN table import_portfolio_result;
	DROP FOREIGN table import_portfolio_esg_score;
	DROP FOREIGN table import_portfolio;
	DROP FOREIGN table import_security_financial_series;
	DROP FOREIGN table import_security;
	DROP FOREIGN table import_company_esg_factor;
	DROP FOREIGN table import_company;
	DROP FOREIGN table import_alert_substitution_value;
	DROP FOREIGN table import_alert_history;

END
$$
LANGUAGE plpgsql;



-------------------------------------------------------------------------------------------------------
-- Step 4: Restore all table data from the FixtureData folder
--
--         To set the root project path in your environment, modify and run the following line:
--
--         SELECT set_config('ssgx.root_path', 'D:/source/InnovationLab/ESG/SourceCode/Back_end/', false)
--
--         This will set the path until the Postgres service is restarted. To permanently set the config 
--         setting, modify the setting below and add it to postgresql.conf (in the data folder of your 
--         PostgreSQL installation folder):
--
--         ssgx.root_path = 'D:/source/InnovationLab/ESG/SourceCode/Back_end/'
-------------------------------------------------------------------------------------------------------
create or replace function get_esg_root_path()
returns varchar
as $$
	BEGIN
		return current_setting('ssgx.root_path');
	END;

$$
LANGUAGE plpgsql;


select * from import_tables_from_csv(get_esg_root_path() || 'data_load/FixtureData/');

-- Encrypt passwords
update membership.login set password = membership.hash_password(password);


-------------------------------------------------------------------------------------------------------
-- Step 5: You should probably run Vacuum to avoid messages about out of date tables. 
--         Needs to be run manually...
-------------------------------------------------------------------------------------------------------
-- vacuum full
