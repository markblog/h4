create or replace function random_string(p_len int default 32)
returns text
as $$
    select substring(md5(random()::text), 0, p_len + 1);
$$
language sql;
