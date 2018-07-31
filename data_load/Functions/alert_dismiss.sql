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

