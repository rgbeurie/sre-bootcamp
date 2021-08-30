import hashlib

import mysql.connector
import jwt

MYSQL_CONFIG = {
    'user': 'secret',
    'password': 'noPow3r',
    'host': 'bootcamp-tht.sre.wize.mx',
    'port': 3306,
    'database': 'bootcamp_tht'
}
JWT_SECRET = 'my2w7wjd7yXF64FIADfJxNs1oupTGAuW'

class Token:

    def generate_token(self, username, password):
        mysql_connection = mysql.connector.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_connection.cursor(dictionary=True)

        query = "SELECT password, salt, role FROM users WHERE username = %(username)s"
        mysql_cursor.execute(query, {'username': username})
        user = mysql_cursor.fetchone()

        if user is None:
            return

        password_hashed = hashlib.sha512((password+user['salt']).encode('utf-8')).hexdigest()

        if password_hashed != user['password']:
            return

        jwt_payload = {
            'role': user['role']
        }
        jwt_response = jwt.encode(jwt_payload, JWT_SECRET, algorithm='HS256')

        return jwt_response


class Restricted:

    def access_data(self, authorization):
        jwt_request = authorization.replace("Bearer ", "")
        try:
            jwt.decode(jwt_request, JWT_SECRET, algorithms='HS256')
        except:
            return

        return "You are under protected data"
