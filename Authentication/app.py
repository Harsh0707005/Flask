from flask import Flask, request, render_template, make_response
import sqlite3
import random
import string

app = Flask(__name__)

connect = sqlite3.connect('users.db')
connect.execute('CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT, sessionId TEXT)')

# generating random session id
def generateRandomNo(n):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return 'Passwords do not match!'

        with sqlite3.connect('users.db') as users:
            cursor = users.cursor()
            cursor.execute('INSERT INTO users(email, password) VALUES(?, ?)', (email, password))
            users.commit()
            return cursor.execute("SELECT * FROM users").fetchall()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('users.db') as users:
            cursor = users.cursor()

            cursor.execute('SELECT * from users WHERE email=?', (email,))
            if cursor.fetchall() !=[]:
                cursor.execute('SELECT * from users WHERE email=? AND password=?', (email, password))
                if cursor.fetchall() != []:
                    sessionId = generateRandomNo(30)
                    cursor.execute('UPDATE users SET sessionID=? WHERE email=?', (sessionId, email))
                    users.commit()

                    response = make_response("Login Successfull")
                    response.set_cookie('sessionId', sessionId)
                    return response
                else:
                    return "Invalid Password"
            else:
                return "User doesn't exist"
        
    return render_template('login.html')
    


if __name__ == '__main__':
    app.run(port=8000, debug=True)