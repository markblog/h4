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
