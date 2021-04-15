"""
THIS MODULE CONTAINS DATABASE ACCESS USING SQLITE3

""" 

import sqlite3
import logging
def sql(sqltext):
    rows = None
    column_names = []
    if len(sqltext) > 0:
        mysql_conn = sqlite3.connect('./fiqs.db')
        my_cursor = mysql_conn.cursor()
        logging.info(sqltext)
        #print(sqltext)
        # sqltext = "select fleet_id, operator_name, fleet_type, capacity, status from fleet"
        my_cursor.execute(sqltext)
        # get the column names
        for c in my_cursor.description:
            column_names.append(c[0])
        # get the data
        rows = my_cursor.fetchall()
        logging.info("Number of Rows fetched "+str(len(rows)))
        #print(column_names)
        #for drow in rows:
        #    print(drow)
    return rows, column_names


# USE THIS BLOCK OF CODE FOR UNIT TESTING OR DEBUGGING
# sqltext = "select fleet_id, operator_name, fleet_type, capacity, status from fleet"
# result = sql(sqltext)
# col_name = []
# for k in result[0]:
#     print(k)
#     col_name.append(k)
# print(col_name[0])


