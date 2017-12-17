import mysql.connector
import csv

def put_info():
	con = mysql.connector.connect(user='sql11206944', password='McQ4scpNVX',
                              host='sql11.freemysqlhosting.net',
                              database='sql11206944')
	cursor = con.cursor()
	
	i = ii = 0 
	reader = csv.reader(open('D:\goods.csv', 'r'),delimiter=";")
	for row in reader:
		i += 1
		if row[1].strip() == "":
			continue
		query = "INSERT INTO gerasymchuk_goods (kod1c,sk,name) VALUES(%s,%s,%s) \
		ON DUPLICATE KEY UPDATE name = %s, sk = %s"
		cursor.execute(query, (row[0], row[1], row[2], row[1], row[2]))
		con.commit()
		if i == 1000:
			i = 0
			ii += 1
			print(ii)
		
	con.close()
	
put_info()	
