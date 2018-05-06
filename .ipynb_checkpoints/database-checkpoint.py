import sqlite3

def create_table():
    # Step 1: Create a connection
    conn=sqlite3.connect("lite.db")
    # Step 2: Create a cursor
    cur=conn.cursor()
    # Step 3: Execute cursor
    cur.execute("CREATE TABLE IF NOT EXISTS houses (title TEXT, locality TEXT, size TEXT, rooms TEXT, price TEXT)")
    # Step 4: Commit
    conn.commit()
    # Step 5: Close connection
    conn.close()

def insert(title,locality,size,rooms,price):
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO houses VALUES (?,?,?,?,?)",(title,locality,size,rooms,price))
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

def update(title,locality,size,rooms,price):
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("UPDATE houses SET title=?, locality=?, size=?, rooms=?, price=? WHERE title=?",(title,locality,size,rooms,price))
    conn.commit()
    conn.close()

create_table()