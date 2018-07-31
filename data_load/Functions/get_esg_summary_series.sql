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
