from etlhelper import DbParams, copy_rows, get_rows
from etlhelper.row_factories import dict_row_factory

sqlite_first = DbParams(dbtype='SQLITE', filename='C:\\Users\\vipin.soni\\db1.db')
sqlite_second = DbParams(dbtype='SQLITE', filename='C:\\Users\\vipin.soni\\db2.db')

select_sql1 = "SELECT * FROM company"
select_sql2 = "SELECT * FROM company2"
select_sql3 = "SELECT * from company WHERE id = :id"

with sqlite_first.connect() as conn_first:
    with sqlite_second.connect() as conn_second:
        # get rows from db
        xx = get_rows(select_sql1, conn_first)
        yy = get_rows(select_sql2, conn_second)
        print(xx, yy)

        zz = get_rows(select_sql3, conn_first, parameters={'id': 1})
        print(zz)

        # dictionary as response
        data_list = []
        for row1 in get_rows(select_sql1,conn_first, row_factory=dict_row_factory):
            data_list.append(row1)
            for row2 in get_rows(select_sql2,conn_second, row_factory=dict_row_factory):
                data_list.append(row2)

        # list contains dictionary
        print(data_list)

