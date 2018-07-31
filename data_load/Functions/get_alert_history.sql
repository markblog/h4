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
