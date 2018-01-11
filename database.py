import sqlite3

def create_table():
    # Step 1: Create a connection
    conn=sqlite3.connect("lite.db")
    # Step 2: Create a cursor
    cur=conn.cursor()
    # Step 3: Execute cursor
    cur.execute("CREATE TABLE IF NOT EXISTS houses (title TEXT, locality TEXT, price TEXT, rooms TEXT, size TEXT, link TEXT)")
    # Step 4: Commit
    conn.commit()
    # Step 5: Close connection
    conn.close()

def insert(title,locality,price,rooms,size,link):
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO houses VALUES (?,?,?,?,?,?)",(title,locality,price,rooms,size,link))
    conn.commit()
    conn.close()

def view():
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM houses")
    rows=cur.fetchall()
    conn.close()
    return rows

def delete(item):
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM houses WHERE title=?",(item,))
    conn.commit()
    conn.close()

def update(locality,price,rooms,size,link,title):
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("UPDATE houses SET locality=?, price=?, rooms=?, size=?, link=?, title=? WHERE title=?",(locality,price,rooms,size,link,title))
    conn.commit()
    conn.close()

create_table()
#print(view())
