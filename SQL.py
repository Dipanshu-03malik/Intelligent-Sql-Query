import sqlite3

# connect sqllite

connection=sqlite3.connect("student.db")

# create a cursor obj to insert the recored, create table,retrieve
cursor=connection.cursor()

#create table

table_info="""
Create table STUDENTSS(NAME VARCHAR(25), CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS int);"""

cursor.execute(table_info)
# insert records

cursor.execute("INSERT INTO STUDENT VALUES('Alice Smith','10th','A',95);")
cursor.execute("INSERT INTO STUDENT VALUES('Bob Johnson','10th','B',88);")
cursor.execute("INSERT INTO STUDENT VALUES('Charlie Brown','9th','A',72);")
cursor.execute("INSERT INTO STUDENT VALUES('Diana Prince','11th','C',91);")
cursor.execute("INSERT INTO STUDENT VALUES('Ethan Hunt','10th','A',78);")
cursor.execute("INSERT INTO STUDENT VALUES('Fiona Green','9th','B',65);")
cursor.execute("INSERT INTO STUDENT VALUES('George White','12th','A',80);")
cursor.execute("INSERT INTO STUDENT VALUES('Hannah Rose','11th','B',93);")
cursor.execute("INSERT INTO STUDENT VALUES('Ivy Black','10th','C',70);")
cursor.execute("INSERT INTO STUDENT VALUES('Jack Ryan','9th','A',85);")
cursor.execute("INSERT INTO STUDENT VALUES('Karen Lee','12th','B',98);")
cursor.execute("INSERT INTO STUDENT VALUES('Liam Miller','11th','A',75);")
cursor.execute("INSERT INTO STUDENT VALUES('Mia Davis','10th','B',90);")
cursor.execute("INSERT INTO STUDENT VALUES('Noah Wilson','9th','C',68);")
cursor.execute("INSERT INTO STUDENT VALUES('Olivia Taylor','12th','C',82);")
cursor.execute("INSERT INTO STUDENT VALUES('Peter Jones','11th','B',79);")
cursor.execute("INSERT INTO STUDENT VALUES('Quinn Martin','10th','A',92);")
cursor.execute("INSERT INTO STUDENT VALUES('Rachel Hall','9th','B',71);")
cursor.execute("INSERT INTO STUDENT VALUES('Sam Baker','12th','A',86);")
cursor.execute("INSERT INTO STUDENT VALUES('Tina Clark','11th','C',94);")
cursor.execute("INSERT INTO STUDENT VALUES('Umar Khan','10th','C',60);")
cursor.execute("INSERT INTO STUDENT VALUES('Vera Singh','9th','A',89);")
cursor.execute("INSERT INTO STUDENT VALUES('Will Turner','12th','B',77);")
cursor.execute("INSERT INTO STUDENT VALUES('Xenia Chen','11th','A',96);")
cursor.execute("INSERT INTO STUDENT VALUES('Yara Lopez','10th','B',83);")

print("Inserted records are ")
data = cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

# close connection

connection.commit()
connection.close()
