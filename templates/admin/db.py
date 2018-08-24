#!/usr/bin/env python
import MySQLdb
# connect to the database
db = MySQLdb.connect("localhost","root","CIACampus@2","users" )
# setup a cursor object using cursor() method
cur = db.cursor()
# run an sql question
cur.execute("SELECT VERSION()")
# grab one result
data = cursor.fetchone()
# begin printing data to the screen
print "Content-Type: text/html"
print

print """\
<html>
<head>
<title>Python - Hello World</title>
</head>
<body>
"""

print "Database version : %s " % data

print"""\
</body>
</html>
"""

# close the mysql database connection
db.close()
