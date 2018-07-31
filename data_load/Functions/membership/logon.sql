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

