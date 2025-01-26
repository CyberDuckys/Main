def database(query):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(str(query))
        mysql.connection.commit()
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print("Error occurred: ", e)