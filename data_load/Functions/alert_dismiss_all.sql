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

