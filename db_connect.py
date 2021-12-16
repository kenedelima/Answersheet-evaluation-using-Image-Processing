import mysql.connector

def connect():
    message = 'success'
    try:
        # conn = sqlite3.connect('db/gui_db.db')
        my_db = mysql.connector.connect(host='localhost',user='root',password="",db="university_db")
        my_cursor = my_db.cursor()
        # my_cursor.execute('show databases')


        # for i in my_cursor:
        #     print(i)
        # cur = db.cursor()

        # Use all the SQL you like
        my_cursor.execute("SELECT * FROM answer_sheet_table_01")
        # print(my_cursor)
        for row in my_cursor.fetchall():
            print(row)

        my_cursor.close()
        

    except:
        message = 'fail'

    return message