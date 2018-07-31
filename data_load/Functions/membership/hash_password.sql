create or replace function hash_password(p_password text)
returns text
as $$
    SELECT membership.crypt(p_password, membership.gen_salt('bf', 10)) 
$$
language sql;
