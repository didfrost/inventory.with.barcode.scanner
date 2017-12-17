import mysql.connector

def get_info():
	con = mysql.connector.connect(user='sql11206944', password='McQ4scpNVX',
                              host='sql11.freemysqlhosting.net',
                              database='sql11206944')
	cursor = con.cursor()
	
	file = open("D:\download_from_mysql.csv",'w')
	row = "%s;%s;%s\n" % ("Код 1С", "Код відділу", "К-сть")
	file.write(row)
	
	query = "Select kod1c, idDep, qty from gerasymchuk_store"
	cursor.execute(query)
	for (kod1c, idDep, qty) in cursor:
		row = "%s;%s;%s\n" % (kod1c, idDep, qty)
		file.write(row)

	con.close()
	file.close()
	
get_info()	
