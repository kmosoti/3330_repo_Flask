import pyodbc 

server = 'art-gallery.cphddxev4bq9.us-east-2.rds.amazonaws.com'
database = "{Art Gallery}"
username = 'UTAStudent05'
password = '3asy-123'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABSE='+database+';UID='+username+';PWD='+password)

cursor = cnxn.cursor()
cursor.execute('Select * from [Art Gallery].dbo.ARTIST')

for i in cursor:
    print(i)

cursor.close()

cnxn.close()