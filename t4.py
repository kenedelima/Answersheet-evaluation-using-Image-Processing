import mysql.connector
import pandas as pd
# def connect():
#     message = 'success'
#     try:
#         # conn = sqlite3.connect('db/gui_db.db')
#         my_db = mysql.connector.connect(host='localhost',user='root',password="",db="university_db")
#         my_cursor = my_db.cursor()
#         # my_cursor.execute('show databases')


#         # for i in my_cursor:
#         #     print(i)
#         # cur = db.cursor()

#         # Use all the SQL you like
#         my_cursor.execute("SELECT * FROM answer_sheet_table_01")
#         # print(my_cursor)
#         for row in my_cursor.fetchall():
#             print(row)

#         my_cursor.close()
        

#     except:
#         message = 'fail'

#     return message
dbcon = mysql.connector.connect(host='localhost',user='root',password="",db="university_db")
SQL_Query = pd.read_sql_query("select * from answer_sheet_table_01 where Answer_Booklet_No='-' or Barcode_No='-' or Roll_No ='-'", dbcon)
df = pd.DataFrame(SQL_Query, columns=['File_Path', 'File','Answer_Booklet_No','Barcode_No','Roll_No'])

df = df['File']
print(df)
my_cursor = dbcon.cursor()
dataFrameCounter = len(df)
index = 0

def updateFunc(dataFrameCounter,index):
    if(dataFrameCounter <=0 ):
        print('Task Finished!')
    else:
        print('Doing Task!')
        sql = f"UPDATE answer_sheet_table_01 SET Answer_Booklet_No = '-',Barcode_No = '-' WHERE File = '{str(df[index])}'"
        my_cursor.execute(sql)
        updateFunc(dataFrameCounter -1,index+1)


updateFunc(dataFrameCounter,index)
dbcon.commit()
# for i in df:
#     print(i,type(i))
#     sql = f"UPDATE answer_sheet_table_01 SET Answer_Booklet_No = '0' WHERE File = '{str(i)}'"

#     my_cursor.execute(sql)

# dbcon.commit()
    

# for i in df:
#     print(i)
# UPDATE table_name SET column1 = value1, column2 = value2 WHERE condition;