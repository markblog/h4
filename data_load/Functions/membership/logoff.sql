drop function if exists membership.logoff(varchar);

create function membership.logoff(p_session_id varchar)
returns void as
$$
    delete from membership.session where id = p_session_id;
$$ LANGUAGE SQL;
