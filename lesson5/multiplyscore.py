import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies
import random

connection = sqlite3.connect('users.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()
if (r == []):
    exp = 'CREATE TABLE users (username,password)'
    connection.execute(exp)


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken. <a href="/">login</a>'.format(un).encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?, ?)', [un, pw])
            connection.commit()
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} Successfully registered. <a href="/">login</a>'.format(un).encode()]
            #[INSERT CODE HERE. Use SQL commands to insert the new username and password into the table that has been created. Print a message saying the username was created successfully]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. <a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password. <a href="/">Login</a>'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()

        #This is where the game begins. This section of is code only executed if the login form works, and if the user is successfully logged in
        if user:
            correct = 0
            wrong = 0

            cookies = http.cookies.SimpleCookie()
            if 'HTTP_COOKIE' in environ:
                cookies.load(environ['HTTP_COOKIE'])
                if un not in cookies:
                    headers.append(('Set-Cookie', '{}={}:{}'.format(un, correct, wrong)))
                else:
                    correct = int(cookies[un].value.split(':')[0])
                    wrong = int(cookies[un].value.split(':')[1])
                #[INSERT CODE FOR COOKIES HERE]

            page = '<!DOCTYPE html><html><head><title>Multiply with Score</title></head><body>'
            if 'factor1' in params and 'factor2' in params and 'answer' in params:
                if int(params['answer'][0]) == int(params['factor1'][0]) * int(params['factor2'][0]):
                    page += '<p style="background-color: lightgreen">Correct, {} x {} = {}</p>'.format(
                            params['factor1'][0], params['factor2'][0], params['answer'][0])

                    correct += 1
                else:
                    page += '<p style="background-color: red">Wrong, {} x {} &#8800; {}</p>'.format(
                        params['factor1'][0], params['factor2'][0], params['answer'][0])
                    wrong += 1
                #[INSERT CODE HERE. If the answer is right, show the “correct” message. If it’s wrong, show the “wrong” message.]

            elif 'reset' in params:
                correct = 0
                wrong = 0

            headers.append(('Set-Cookie', '{}={}:{}'.format(un, correct, wrong)))

            f1 = random.randrange(10) + 1
            f2 = random.randrange(10) + 1

            page = page + '<h1>What is {} x {}</h1>'.format(f1, f2)
            bot = f1 * f2
            choices = [bot, random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
            #[INSERT CODE HERE. Create a list that stores f1*f2 (the right answer) and 3 other random answers]
            random.shuffle(choices)

            hyperlink = '<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}: {}</a><br>'
            page += hyperlink.format(un, pw, f1, f2, choices[0], 'A', choices[0])
            page += hyperlink.format(un, pw, f1, f2, choices[1], 'B', choices[1])
            page += hyperlink.format(un, pw, f1, f2, choices[2], 'C', choices[2])
            page += hyperlink.format(un, pw, f1, f2, choices[3], 'D', choices[3])
            #[INSERT CODE HERE. Create the 4 answer hyperlinks here using string formatting.]

            page += '''<h2>Score</h2>
            Correct: {}<br>
            Wrong: {}<br>
            <a href="/account?reset=true">Reset</a>
            <br>
            <a href="/logout">Logout</a>
            </body></html>'''.format(correct, wrong)

            return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

    elif path == '/':
        page = '''<!DOCTYPE html>
            <html>
            <head><title>Login or Register</title></head>
            <body>
            <h1>Login</h1>
            <form action="/login">
            Username <input type="text" name="username"><br>
            Password <input type="password" name="password"><br>
            <input type="submit" value="Login">
            </form>
            <h1>Register</h1>
            <form action="/register">
            Username <input type="text" name="username"><br>
            Password <input type="password" name="password"><br>
            <input type="submit" value="Register">
            </form>
            <br>
            </body>
            </html>'''
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [page.encode()]
        #[INSERT CODE HERE. Create the two forms, one to login, the other to register a new account]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()