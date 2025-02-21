import sqlite3
db_file = 'prices.db'

def createConnection():
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print("connection failed")

def closeConnection(conn):
    if conn:
        conn.close()

def checkProductExists(ID):
    try:
        conn = createConnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Products WHERE ProductID = ?",(ID,))
        product = cur.fetchone()
        closeConnection(conn)
        if product is None:
            return False
        return True
    except sqlite3.Error as e:
        closeConnection(conn)
        raise Exception("Error during checking product")



def createNewProduct(Product_Name,ID):
    try:
        conn = createConnection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Products(Name,ProductID) VALUES(?,?)",(Product_Name,ID))
        conn.commit()
        closeConnection(conn)
        return True
    except sqlite3.Error as e:
        closeConnection(conn)
        raise Exception("Error during product creation")
    
def addprice(ID,Price,Date):
    try:
        conn = createConnection()
        cur = conn.cursor()
        cur.execute("INSERT INTO ProductPrice(ProductID,Price,Date) VALUES(?,?,?)",(ID,Price,Date))
        conn.commit()
        closeConnection(conn)
        return True
    except sqlite3.Error as e:
        closeConnection(conn)
        raise Exception("Error during price entry")