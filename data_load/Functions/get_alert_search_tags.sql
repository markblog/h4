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
