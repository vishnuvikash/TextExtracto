def populatedb(l):
        import sqlite3
        conn = sqlite3.connect('normanpd.db')
        c=conn.cursor()
        c.executemany('INSERT INTO incidents VALUES (?,?,?,?,?,?)',l)
        print("Database populated succesfuly!!!")
        conn.commit()
        conn.close()
        
