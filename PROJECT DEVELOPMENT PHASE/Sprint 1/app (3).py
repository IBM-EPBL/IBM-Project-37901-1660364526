from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db 
import re
 
app = Flask(__name__)
  
app.secret_key = 'a'

conn = ibm_db.connect('DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cgm44134;PWD=pbnfcEGlumRQcMHo;','','')
     
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM signup WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO signup VALUES(?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully signedup!'
            return render_template('register.html',msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg)


@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        email = request.form['eamil']
        password = request.form['password']
        sql = "SELECT * FROM signup WHERE email =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if not(account):
            session['loggedin'] = True
            session['id'] = account['EMAIL']
            userid=  account['EMAIL']
            session['email'] = account['EMAIL']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
               msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

         
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        height = request.form['height']
        weight = request.form['weight']
        age = request.form['age']
        illness = request.form['illness']
        gender = request.form['gender']
        allergies = request.form['allergy']
        sql = "SELECT * FROM profile WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if not(account):
            insert_sql = "INSERT INTO  profile VALUES (?, ?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, height)
            ibm_db.bind_param(prep_stmt, 3, weight)
            ibm_db.bind_param(prep_stmt, 4, age)
            ibm_db.bind_param(prep_stmt, 5, illness)
            ibm_db.bind_param(prep_stmt, 6, gender)
            ibm_db.bind_param(prep_stmt, 7, allergies)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('main.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/card')
def card():
        #print(session["FOOD"],session['id'])
        sql = "SELECT * FROM INGREDIANT WHERE FOOD =?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,"Almonds" )
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print("accountcard",account)
        return render_template('card.html',account = account)



if __name__ == '__main__':
   app.run(debug=True)
   