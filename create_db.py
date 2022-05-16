import sqlite3

conn=sqlite3.connect('sqlite.db')

conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS userInfo (
        id String(50) primary key, 
        sub_id String(50), 
        pwd String(50), 
        email String(50), 
        phone_number String(50) 
    )
    '''
)
print("ok")
conn.close()