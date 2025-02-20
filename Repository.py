import sqlite3
db_file = 'price.db'
from flask import jsonify,abort

def createConnection():
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("connection to database complete")
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
        if product == None:
            return False
        return True
    except sqlite3.Error as e:
        closeConnection(conn)
        return abort(404,description = 'Error occured during execution')



def createNewProduct(Product_Name,ID):
    try:
        conn = createConnection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Products(Product_Name,ID) VALUES(?,?)",(Product_Name,ID))
        conn.commit()
        closeConnection(conn)
        return jsonify({'message':'OK'}),200
    except sqlite3.Error as e:
        closeConnection(conn)
        return abort(404,description = 'Error occured during execution')
    
def addprice(ID,Price,Date):
    try:
        conn = createConnection()
        cur = conn.cursor()
        cur.execute("INSERT INTO ProductPrice(ProductID,Price,Date) VALUES(?,?,?)",(ID,Price,Date))
        conn.commit()
        closeConnection(conn)
        return jsonify({'message':'OK'}),200
    except sqlite3.Error as e:
        closeConnection(conn)
        return abort(404,description = 'Error occured during execution')