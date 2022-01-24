# Dołączanie modułu flask 

from gettext import NullTranslations
from pydoc import describe
from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from flask import Flask, session
from flask_session import Session
import sqlite3

# Tworzenie aplikacji
app = Flask("Flask - Lab")

# Tworzenie obsługi sesji
sess = Session()

# Ścieżka do pliku bazy danych w sqlite
DATABASE = 'database.db'



@app.route('/create_database', methods=['GET', 'POST'])
def create_db():
    # Połączenie sie z bazą danych
    conn = sqlite3.connect(DATABASE)
    # Stworzenie tabeli w bazie danych za pomocą sqlite3
    conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)')
    conn.execute('CREATE TABLE notices (id INTEGER PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL, price FLOAT NOT NULL, id_buyer INTEGER, id_seller INTEGER NOT NULL)')
    # Zakończenie połączenia z bazą danych
    conn.close()
    
    return index()

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if 'user' in session:   
        con = sqlite3.connect(DATABASE)    
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall(); 
        if len(users)<=0:
            con = sqlite3.connect(DATABASE)
            # Pobranie danych z tabeli
            cur = con.cursor()
            cur.execute("select * from notices where id_buyer is null")
            notices = cur.fetchall(); 
            return render_template('general.html', notices = notices, user = False)
        else: 
            con = sqlite3.connect(DATABASE)
            # Pobranie danych z tabeli
            cur = con.cursor()
            cur.execute("select * from notices where id_buyer is null and id_seller!=?",(users[0][0],))
            notices = cur.fetchall(); 
            return render_template('general.html', notices = notices, user = True)
    else:
        con = sqlite3.connect(DATABASE)
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from notices where id_buyer is null")
        notices = cur.fetchall(); 
        return render_template('general.html', notices = notices, user = False)
    
@app.route('/my_notices', methods=['GET', 'POST'])
def myNotices(): 
    if 'user' in session:   
        con = sqlite3.connect(DATABASE)    
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall(); 
        if len(users)<=0:
            return redirect(url_for('index'))
        else: 
            con = sqlite3.connect(DATABASE)
            # Pobranie danych z tabeli
            cur = con.cursor()
            cur.execute("select * from notices where id_seller==? and id_buyer is null",(users[0][0],))
            notices = cur.fetchall(); 
            return render_template('myNotices.html', notices = notices)
    else:
        return redirect(url_for('index'))    
    
@app.route('/solded_notices', methods=['GET', 'POST'])
def soldedNotices(): 
    if 'user' in session:   
        con = sqlite3.connect(DATABASE)    
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall(); 
        if len(users)<=0:
            return redirect(url_for('index'))
        else: 
            con = sqlite3.connect(DATABASE)
            # Pobranie danych z tabeli
            cur = con.cursor()
            cur.execute("select * from notices where id_seller==? and id_buyer is not null",(users[0][0],))
            notices = cur.fetchall(); 
            return render_template('soldedNotices.html', notices = notices)
    else:
        return redirect(url_for('index'))    

@app.route('/my_shopping', methods=['GET', 'POST'])
def myShopping(): 
    if 'user' in session:   
        con = sqlite3.connect(DATABASE)    
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall(); 
        if len(users)<=0:
            return redirect(url_for('index'))
        else: 
            con = sqlite3.connect(DATABASE)
            # Pobranie danych z tabeli
            cur = con.cursor()
            cur.execute("select * from notices where id_buyer==?",(users[0][0],))
            notices = cur.fetchall(); 
            return render_template('myShopping.html', notices = notices)
    else:
        return redirect(url_for('index'))

@app.route('/new_notice', methods=['GET', 'POST'])
def newNotice():
    if 'user' in session: 
        con = sqlite3.connect(DATABASE)
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall(); 
        if len(users)<=0:
            return redirect(url_for('index'))
        else: 
            return render_template('newNotice.html')
    else:
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def loginForm():
    if 'user' in session:
        con = sqlite3.connect(DATABASE)
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from notices")
        notices = cur.fetchall();       
        con = sqlite3.connect(DATABASE)
    
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall(); 
        if len(users)<=0:
            return render_template('login.html')
        else: 
            return redirect(url_for('index'))
    else:
        return render_template('login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def registerForm():
    if 'user' in session:
        # Pobranie danych z tabeli        
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("select * from notices")
        notices = cur.fetchall();       
        con = sqlite3.connect(DATABASE)
    
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall(); 
        if len(users)<=0:
            return render_template('register.html')
        else: 
            return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/login_user', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    
    con = sqlite3.connect(DATABASE)
    
    # Pobranie danych z tabeli
    cur = con.cursor()
    cur.execute("select * from users where username=? and password=?",(login,password))
    users = cur.fetchall(); 
    if users:
        # Stworzenie sesji dla kilenta i dodanie pola user
        session['user']=login
    
    # Przekierowanie klienta do strony początkowej
    return redirect(url_for('index'))


@app.route('/add_user', methods=['POST'])
def addUser():
        login = request.form['login']
        password = request.form['password']
        passwordRepeat  = request.form.get('password2',False)

        # Dodanie użytkownika do bazy danych
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)",(login,password) )
        con.commit()
        con.close()

        return index()

@app.route('/add_notice', methods=['POST'])
def addNotice():
    if 'user' in session:
        description = request.form['description']
        title = request.form['title']        
        price = request.form['price']

        # Dodanie ogłoszenia do bazy danych
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall(); 
        if len(users)>0:
            cur.execute("INSERT INTO notices (title,description,price,id_seller) VALUES (?,?,?,?)",(title, description, price, users[0][0]))
        con.commit()
        con.close()

    # Przekierowanie klienta do strony początkowej
    return redirect(url_for('myNotices'))

# Endpoint umożliwiający podanie parametru w postaci string'a
@app.route('/delete/<noticeId>')
def deleteNotice(noticeId):
    if 'user' in session: 
        con = sqlite3.connect(DATABASE)
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall(); 
        if len(users)<=0:
            return redirect(url_for('index'))
        else: 
            con = sqlite3.connect(DATABASE)
            con.execute("delete from notices where id=?",(noticeId,))
            con.commit()
            con.close()
            return redirect(url_for('myNotices'))
    else:
        return redirect(url_for('index'))

# Endpoint umożliwiający podanie parametru w postaci string'a    
@app.route('/update/<noticeId>', methods=['POST'])
def updateNotice(noticeId):
    if 'user' in session: 
        description = request.form['description']
        title = request.form['title']        
        price = request.form['price']
        con = sqlite3.connect(DATABASE)
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall()
        if len(users)<=0:
            return redirect(url_for('index'))
        else:             
            con = sqlite3.connect(DATABASE)
            con.execute("update notices set title=?, description=?, price=? where id=?",(title,description,price,noticeId,))
            con.commit()
            con.close()
            return redirect(url_for('myNotices'))
    else:
        return redirect(url_for('index'))

# Endpoint umożliwiający podanie parametru w postaci string'a
@app.route('/edit/<noticeId>')
def editNotice(noticeId):
    if 'user' in session: 
        con = sqlite3.connect(DATABASE)
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall()
        if len(users)<=0:
            return redirect(url_for('index'))
        else: 
            con = sqlite3.connect(DATABASE)
            # Pobranie danych z tabeli
            cur = con.cursor()
            cur.execute("select * from notices where id=?",(noticeId,))
            notices = cur.fetchall()
            if len(notices)<=0:
                return redirect(url_for('myNotices'))
            else:
                return render_template('editNotice.html', notice = notices[0])
    else:
        return redirect(url_for('index'))
    
# Endpoint umożliwiający podanie parametru w postaci string'a
@app.route('/buy/<noticeId>')
def buyNotice(noticeId):
    if 'user' in session: 
        con = sqlite3.connect(DATABASE)
        # Pobranie danych z tabeli
        cur = con.cursor()
        cur.execute("select * from users where username=?",(session['user'],))
        users = cur.fetchall()
        if len(users)<=0:
            return redirect(url_for('index'))
        else: 
            con = sqlite3.connect(DATABASE)
            con.execute("update notices set id_buyer=? where id=?",(users[0][0],noticeId,))
            con.commit()
            con.close()
            return redirect(url_for('myShopping'))
    else:
        return redirect(url_for('index'))    

@app.route('/logout', methods=['GET'])
def logout():
    # Jeżeli sesja klienta istnieje - usunięcie sesji 
    if 'user' in session:
        session.pop('user')
        
    return redirect(url_for('index'))

# Uruchomienie aplikacji w trybie debug
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)
app.config.from_object(__name__)
app.debug = True
app.run()