create or replace function alert_mark_all_read(p_login_id int)
returns void as
$$
BEGIN

    insert into alert_digest_history (alert_history_id, login_id, is_dismissed)
    select distinct alert_history_id, p_login_id, False 
    from get_alert_history(p_login_id) h where h.alert_history_id not in (select alert_history_id from alert_digest_history where login_id = p_login_id);

END;
$$ LANGUAGE plpgsql;
