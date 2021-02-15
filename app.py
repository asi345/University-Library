import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from forms import BookSearchForm, UserSearchForm, BorrowSearchForm
from init_db import listbooks

def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection

app = Flask(__name__)
app.config["SECRET_KEY"] = "cmpe321"

@app.route("/")
def index() :
    return render_template("index.html")

@app.route("/listbooks", methods=('GET', 'POST'))
def listbooks():
    connection = get_db_connection()
    search = BookSearchForm(request.form)
    books = []
    if request.method == 'POST' :
        books = connection.execute('SELECT * FROM BOOK WHERE {} LIKE "%{}%"'.format(search.data['select'], search.data['search'])).fetchall() 
    else :
        books = connection.execute('SELECT * FROM BOOK').fetchall()
    connection.commit()
    connection.close()
    return render_template('listbooks.html', books=books, form=search)


@app.route('/createbook', methods=('GET', 'POST'))
def createbook():
    isempty = False
    if request.method == 'POST':
        isbn = request.form['ISBN']
        title = request.form['Title']
        author = request.form['Author']
        if not isbn or not title or not author :
            isempty = True
        else :
            connection = get_db_connection()
            connection.execute('INSERT INTO BOOK (ISBN, Title, Author) VALUES (?, ?, ?)',
                         (isbn, title, author))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    return render_template('createbook.html', isempty=isempty)

@app.route('/deletebook', methods=('GET', 'POST'))
def deletebook():
    isempty = False
    if request.method == 'POST' :
        isbn = request.form['ISBN']
        if not isbn :
            isempty = True
        else :
            connection = get_db_connection()
            connection.execute('DELETE FROM BOOK WHERE ISBN = ?', (isbn,))
            connection.commit()
            connection.close() 
            return redirect(url_for('index'))
    return render_template('deletebook.html', isempty=isempty)

@app.route("/listusers", methods=('GET', 'POST'))
def listusers():
    connection = get_db_connection()
    search = UserSearchForm(request.form)
    users = []
    if request.method == 'POST' :
        users = connection.execute('SELECT * FROM USER WHERE {} LIKE "%{}%"'.format(search.data['select'], search.data['search'])).fetchall() 
    else :
        users = connection.execute('SELECT * FROM USER').fetchall()
    connection.commit()
    connection.close()
    return render_template('listusers.html', users=users, form=search)

@app.route('/createuser', methods=('GET', 'POST'))
def createuser():
    isempty = False
    if request.method == 'POST':
        tcno = request.form['TCNO']
        firstname = request.form['FIRSTNAME']
        lastname = request.form['LASTNAME']
        if not tcno or not firstname or not lastname :
            isempty = True
        else :
            connection = get_db_connection()
            connection.execute('INSERT INTO USER (TCNO, FIRSTNAME, LASTNAME) VALUES (?, ?, ?)',
                         (tcno, firstname, lastname))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    return render_template('createuser.html', isempty=isempty)

@app.route('/deleteuser', methods=('GET', 'POST'))
def deleteuser():
    isempty = False
    if request.method == 'POST' :
        tcno = request.form['TCNO']
        if not tcno :
            isempty = True
        else :
            connection = get_db_connection()
            connection.execute('DELETE FROM USER WHERE TCNO = ?', (tcno,))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    return render_template('deleteuser.html', isempty=isempty)

@app.route("/listborrows", methods=('GET', 'POST'))
def listborrows():
    connection = get_db_connection()
    search = BorrowSearchForm(request.form)
    borrows = []
    if request.method == 'POST' :
        borrows = connection.execute('SELECT * FROM BORROW WHERE {} LIKE "%{}%"'.format(search.data['select'], search.data['search'])).fetchall() 
    else :
        borrows = connection.execute('SELECT * FROM BORROW').fetchall()
    connection.commit()
    connection.close()
    return render_template('listborrows.html', borrows=borrows, form=search)

@app.route('/createborrow', methods=('GET', 'POST'))
def createborrow():
    isempty = False
    isborrowable = True
    if request.method == 'POST':
        isbn = request.form['ISBN']
        tcno = request.form['TCNO']
        if not isbn or not tcno :
            isempty = True
        else :
            connection = get_db_connection()
            num = connection.execute('SELECT NUMOFBOOKS FROM USER WHERE USER.TCNO = ?',
                    (tcno,)).fetchone()
            if ((tuple(num))[0] == 8) :
                isborrowable = False
                return render_template('createborrow.html', isempty=isempty, isborrowable=isborrowable)
            connection.execute('INSERT INTO BORROW (ISBN, TCNO) VALUES (?, ?)',
                         (isbn, tcno))
            connection.execute('''UPDATE USER
                    SET NUMOFBOOKS = NUMOFBOOKS + 1
                    WHERE TCNO = ?''', (tcno,))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    return render_template('createborrow.html', isempty=isempty, isborrowable=isborrowable)

@app.route('/deleteborrow', methods=('GET', 'POST'))
def deleteborrow():
    isempty = False
    if request.method == 'POST' :
        isbn = request.form['ISBN']
        if not isbn :
            isempty = True
        else :
            connection = get_db_connection()
            connection.execute('''UPDATE USER
                    SET NUMOFBOOKS = NUMOFBOOKS - 1
                    WHERE TCNO IN (SELECT TCNO
                        FROM BORROW
                        WHERE ISBN = ?)''', (isbn,))
            connection.execute('DELETE FROM BORROW WHERE ISBN = ?', (isbn,)) 
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    return render_template('deleteborrow.html', isempty=isempty)
