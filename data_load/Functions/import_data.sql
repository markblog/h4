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
