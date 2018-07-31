"C:\Program Files\PostgreSQL\9.5\bin\dropdb.exe" -i -Upostgres esg
"C:\Program Files\PostgreSQL\9.5\bin\pg_restore.exe" -Upostgres -C -d postgres  db.dump
