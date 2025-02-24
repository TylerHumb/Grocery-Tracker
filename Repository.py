import pyodbc

# SQL server string, hosted on SQL express
connectionString = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=Woolworths-Prices;Trusted_Connection=yes;'

def createConnection():
    try:
        conn = pyodbc.connect(connectionString)
        return conn
    except pyodbc.Error as e:
        print("Connection failed:", e)
        return None

def closeConnection(conn):
    if conn is not None:
        conn.close()

def checkProductExists(ID,conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Products WHERE ProductID = ?", (ID,))
        product = cur.fetchone()
        
        return product is not None
    except pyodbc.Error as e:
        print("Error during checking product:", e)
        raise

def createNewProduct(Product_Name, ID,conn):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Products(Name, ProductID) VALUES(?, ?)", (Product_Name, ID))
        conn.commit()
        return True
    except pyodbc.Error as e:
        print("Error during product creation:", e)
        raise

def addprice(ID, Price, Date,conn):
    try:
        cur = conn.cursor()
        #check if price has changes since last check
        cur.execute("SELECT TOP 1 Price FROM ProductPrice WHERE ProductID = ? ORDER BY Date DESC", (ID,))
        lastprice = cur.fetchone()
        # if last price is same a current price, exit function
        if lastprice and lastprice[0] == str(Price):
            return True 

        cur.execute("INSERT INTO ProductPrice(ProductID, Price, Date) VALUES(?, ?, ?)", (ID, Price, Date))
        conn.commit()
        return True
    except pyodbc.Error as e:
        print("Error during price entry:", e)
        raise