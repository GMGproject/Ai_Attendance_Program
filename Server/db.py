import mysql.connector

# Connect to MySQL DB
def connectDB():
    try:
        db = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="1234",
            auth_plugin='mysql_native_password',
            database="AttendanceProgram")

        return db
    except Exception as e:
        print("Connection Error : " , e)

# Disconnect with connected DB
def disconnectDB(db):
    db.close()

# query for Insert, Update, Delete
def queryIUD(sql):
    try:
        db = connectDB()
        cursor = db.cursor()    
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
    finally:
        disconnectDB(db)

# query for Select & print Selected Data
def queryS(sql):
    try:
        db = connectDB()
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        return result
    except Exception as e:
        print(e)
    finally:
        disconnectDB(db)

