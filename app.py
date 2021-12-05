from flask import Flask, redirect, url_for, render_template, request
from flask.wrappers import Response
import pyodbc
from random import randint

server = 'art-gallery.cphddxev4bq9.us-east-2.rds.amazonaws.com'
database = 'Art Gallery'
username = 'UTAStudent05'
password = '3asy-123'

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/insert")
def insert():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABSE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execute('SELECT aID FROM [Art Gallery].dbo.ARTIST')
    result = cursor.fetchall()
    cursor.close()

    a_name = request.form.get("a_name")
    a_birth = request.form.get("a_birth")
    commission = request.form.get("commission")

    print(result)
    return render_template("/executes/insert.html")

@app.route("/update")
def update():
    return render_template("/executes/update.html")

@app.route("/delete")
def delete():
    return render_template("/executes/delete.html")

@app.route("/displaytable", methods=["POST"])
def displayTable():
    aID = request.form.get("a_city")
    name = request.form.get("a_name")
    commission = request.form.get("commission")

    query2 = "SELECT * FROM [Art Gallery].dbo.ARTIST WHERE city LIKE '%{}%' AND name LIKE '%{}%' AND commission LIKE '%{}%'".format(aID, name, commission)
    #query = "SELECT * FROM [Art Gallery].dbo.ARTIST"
    #print(query2)
    result = getData(query2)
    #print(result)
    response = "Displaying Table"
    return render_template('displaytable.html', result=result, response=response)

@app.route("/insertData",  methods=["POST"])
def insertData():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABSE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execute('SELECT aID FROM [Art Gallery].dbo.ARTIST')
    result = cursor.fetchall()
    cursor.close()

    aID = getID(result)
    a_name = request.form.get("a_name")
    a_birth = request.form.get("a_birth")
    commission = request.form.get("commission")
    insertData(aID, a_name, a_birth, commission)
    response = "Inserted artist with aID = "+'{}'.format(aID)
    getRow = getData("SELECT * FROM [Art Gallery].dbo.ARTIST where aID = {}".format(aID))
    print(type(a_birth))
    return render_template('displaytable.html', result=getRow, response=response)

@app.route("/deleteRecord", methods=["POST"])
def deleteRecord():
    aID = request.form.get("aID")
    getRow = getData("SELECT * FROM [Art Gallery].dbo.ARTIST where aID = {}".format(aID))
    deleteRecordCall(aID)
    response = "Deleted Artist With ID = {}".format(aID)
    return render_template('displaytable.html', result=getRow, response=response)
if __name__ == "__main__":
    app.run()

@app.route("/updateRecord", methods=["POST"])
def updateRecord():
    aID = request.form.get("aID")
    newValue = request.form.get("newVal")
    attribute = request.form.get("attribute")

    updateRecordCall(aID,newValue,attribute)
    getRow = getData("SELECT * FROM [Art Gallery].dbo.ARTIST where aID = {}".format(aID))
    response = f"Update Artist[{aID}] {attribute} to {newValue}"
    return render_template('displaytable.html', result=getRow, response=response)
if __name__ == "__main__":
    app.run()

def getData(query):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABSE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    print(query)
    return result

def insertData(aID, name, birthDate, commission):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABSE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    sqlInsert = "INSERT INTO [Art Gallery].dbo.ARTIST(aID, name, birthDate, deathDate, commission, street, city, stateAB, zipcode) VALUES"
    sqlValues = f"({aID},'{name}','{birthDate}',NULL,'{commission}','','','TX','76621-0057')"
    finalQuery = sqlInsert+sqlValues
    print("\n\n"+finalQuery+"\n\n")
    cursor.execute(finalQuery)
    cursor.commit()

def deleteRecordCall(aID):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABSE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    sqlDelete  = "DELETE FROM [Art Gallery].dbo.ARTIST WHERE aID = '{}'".format(aID)
    print("\n\n"+sqlDelete+"\n\n")
    cursor.execute(sqlDelete)
    cursor.commit()

def updateRecordCall(aID,newVal,attribute):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABSE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    sqlUpdate = f"UPDATE [Art Gallery].dbo.ARTIST SET [{attribute}] = '{newVal}' WHERE aID = '{aID}'"
    print("\n\n"+sqlUpdate+"\n\n")
    cursor.execute(sqlUpdate)
    cursor.commit()

def getID(quest):
    aID = randint(0,200)
    if aID in quest:
        aID=getID(aID)
        
    return aID

