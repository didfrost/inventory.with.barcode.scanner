import sqlite3 as lite
import csv

DATABASE = "test.db"
 
def create_table(name,qtable):
	con = lite.connect(DATABASE)
	cur = con.cursor()    
	
	with con:
		cur.execute(qtable)
		print("Created table " + name)

	cleartable = "delete from " + name
	with con:
		cur.execute(cleartable)
		
	con.close()	
		
	
def create_deps():
	con = lite.connect(DATABASE)
	cur = con.cursor()    

	cleartable = "delete from departments"
	with con:
		cur.execute(cleartable)
		
	reader = csv.reader(open('D:\departments.csv', 'r'),delimiter=";")
	for row in reader:
		name = "department"+row[0]
		qtable = "CREATE TABLE IF NOT EXISTS "+name+" (id Integer PRIMARY KEY AUTOINCREMENT, timecreate DateTime, timeupdate DateTime, kod1c Integer, sk Text, qty Double, idDep integer)"
		create_table(name, qtable)
	
		iquery = "Insert into departments  (id,name) values ("+row[0]+",'"+row[1]+"')"
		with con:
			cur.execute(iquery)
			
	con.close()		
			
def fill_goods():
	con = lite.connect(DATABASE)
	cur = con.cursor()    
	cleartable = "delete from goods"
	with con:
		cur.execute(cleartable)
		
	i = ii = 0 
	reader = csv.reader(open('D:\goods.csv', 'r'),delimiter=";")
	for row in reader:
		i += 1
		name = row[2]
		name = name.replace("'","`")
		qtable = "insert or replace into goods (sk,kod1c,name) values ('"+row[1]+"','"+row[0]+"','"+name+"')"
		cur.execute(qtable)
		con.commit()
		if i == 1000:
			i = 0
			ii += 1
			print(ii)
	
# Створимо відділи
create_deps()

# Заповнимо товарами
# fill_goods()



	
 