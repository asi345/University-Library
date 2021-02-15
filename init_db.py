import sqlite3
from datetime import datetime, timedelta

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS BOOK;")
cursor.execute("""CREATE TABLE BOOK (
ISBN    BIGINT  NOT NULL,
Title   VARCHAR(20) NOT NULL,
Author  VARCHAR(20) NOT NULL,
PRIMARY KEY(ISBN));""")

cursor.execute("DROP TABLE IF EXISTS USER;")
cursor.execute("""CREATE TABLE USER (
TCNO    BIGINT  NOT NULL,
FIRSTNAME   VARCHAR(10) NOT NULL,
LASTNAME    VARCHAR(15) NOT NULL,
NUMOFBOOKS  INT NOT NULL    DEFAULT 0,
PRIMARY KEY(TCNO));""")

curDate = datetime.today()
due = timedelta(days=14)
dueDate = (curDate + due).strftime('%Y%m%d')

cursor.execute("DROP TABLE IF EXISTS BORROW;")
cursor.execute("""CREATE TABLE BORROW (
ISBN    BIGINT  NOT NULL,
TCNO    BIGINT  NOT NULL,
DUEDATE DATE    NOT NULL    DEFAULT {},
PRIMARY KEY(ISBN));""".format(dueDate))

cursor.execute("DROP TRIGGER IF EXISTS BOOKDELETED;")
cursor.execute("""CREATE TRIGGER BOOKDELETED
AFTER DELETE
ON BOOK
BEGIN
UPDATE USER
SET NUMOFBOOKS = NUMOFBOOKS - 1
WHERE TCNO IN (SELECT TCNO
    FROM BORROW
    WHERE ISBN = OLD.ISBN);
DELETE FROM BORROW WHERE BORROW.ISBN=OLD.ISBN;
END;""")

cursor.execute("DROP TRIGGER IF EXISTS USERDELETED;")
cursor.execute("""CREATE TRIGGER USERDELETED
AFTER DELETE
ON USER
BEGIN
DELETE FROM BORROW WHERE BORROW.TCNO=OLD.TCNO;
END;""")

procedure = """CREATE PROCEDURE AS LISTBOOKS
AS
SELECT * FROM BOOK;
GO;"""

def listbooks() :
    return connection.execute(procedure[procedure.index("SELECT"):procedure.index("GO") - 1]).fetchall()

connection.commit()
connection.close()
