from mysql.connector import (connection)

config = {'user': 'root',  'password': 'mySQ909L_0', 'database': 'liberverto', 'host': 'localhost','auth_plugin':'mysql_native_password', 'ssl_disabled': False}
try:
    cnx = connection.MySQLConnection(**config)
    cur = cnx.cursor(dictionary=True)
except Exception as e:
    print(e)
    


