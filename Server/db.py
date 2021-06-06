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
def queryIUD(cursor, sql):
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)

# query for Select & print Selected Data
def queryS(cursor, sql):
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for column in result:
            print(column)
    except Exception as e:
        print(e)

# Parse sql to check type & help to do their each part 
def queryExecutor(sql):
    db = connectDB()
    cursor = db.cursor()
    type = sql.split(' ')[0]

    if type.upper() == 'SELECT':
        queryS(cursor, sql)
    else:
        queryIUD(cursor, sql)
        db.commit()

    disconnectDB(db)
