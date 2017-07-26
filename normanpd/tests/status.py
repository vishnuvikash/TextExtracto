import sqlite3


def status(db):
        conn=sqlite3.connect(db)
        print('Connected succesfully to the Database')
        c=conn.cursor()
        c.execute("SELECT COUNT(*) FROM incidents")
        total_row_count=c.fetchone()[0]
        print('\nThe total number of rows in incidents table are {0}\n\n'.format(total_row_count))
        print('Random Five rows from normanpd.db database:\n')
        c.execute("SELECT * FROM incidents ORDER BY RANDOM() LIMIT 5;")
        for row in c.fetchall():
               print(row)
        conn.commit()
        conn.close()
        
        
