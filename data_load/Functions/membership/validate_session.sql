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
