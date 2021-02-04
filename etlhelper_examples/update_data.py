from etlhelper import executemany, DbParams, get_rows

sqlite_first = DbParams(dbtype='SQLITE', filename='C:\\Users\\vipin.soni\\db1.db')
sqlite_second = DbParams(dbtype='SQLITE', filename='C:\\Users\\vipin.soni\\db2.db')

rows = [(5, 'vinay'), (6, 'rohit')]
insert_sql = "INSERT INTO company (id, name) VALUES (?, ?)"

select_sql = "SELECT * from company"

with sqlite_first.connect() as conn:
    executemany(insert_sql, conn, rows)
    xx = get_rows(select_sql,conn)
    print(xx)
