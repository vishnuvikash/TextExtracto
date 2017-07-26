import sqlite3
conn=sqlite3.connect('normanpd.db')
print("Database created and opened succesfully")
c = conn.cursor()


c.execute('''CREATE TABLE incidents
       (id INT PRIMARY KEY NOT NULL,
	number TEXT,
	date_time TEXT,
	location TEXT,
	nature TEXT,	
	ORI TEXT);''')

conn.commit()

conn.close()
