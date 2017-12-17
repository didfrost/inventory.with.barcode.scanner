from flask import Flask, request, render_template, json, g, redirect, url_for
from flask_wtf import FlaskForm
import sqlite3 as lite
import sys
import mysql.connector
import datetime
#from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisismysupersecrectkey'
app.debug = True
#toolbar = DebugToolbarExtension(app)

DATABASE = 'test.db'

# looking for curent department
def getCurrentDepartment():
	constDep = "Department"

	curDep = query_db('select c.valueInt, d.name from constants c, departments d where c.name = ? and d.id = c.valueInt',
					[constDep], one=True)
					
	if curDep is not None:
		con = lite.connect(DATABASE)
		cur = con.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS department"+str(curDep[0]) +"(idDep Integer, kod1c Integer, sk Text, qty Double)");
		con.commit()
		con.close()
		
	return curDep

# working with DATABASE sqlite
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = lite.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
		
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/changeSku', methods=['POST'])
def changeSku():
	data = request.get_json()
	kod1c = data['kod1c']
	sk = data['sk']
	qty = data['qty']
	idRow = data['idRow']
	if qty == "": qty = '0'

	curDep = getCurrentDepartment()
	currentDepId = curDep[0]
	department000 = "department"+str(currentDepId);

	rowq = query_db('select * from '+department000+' where sk = ?',
					[sk], one=True)
	if rowq is None:
		return ""
	else:
		query = "UPDATE "+department000+" SET qty = "+qty+" where id = '"+idRow+"'"
	
	con = lite.connect(DATABASE)
	with con:
		cur = con.cursor()    
		cur.execute(query)
		cur.close()
	con.close()	

	updateDep000(department000,currentDepId)
		
	return "";

@app.route('/addSku', methods=['POST'])
def addSku():
	data = request.get_json()
	kod1c = data['kod1c']
	sk = data['sk']
	qty = data['qty']
	if qty == "": qty = '0'

	curDep = getCurrentDepartment()
	currentDepId = curDep[0]
	department000 = "department"+str(currentDepId);

	rowq = query_db('select * from '+department000+' where kod1c = ?',
					[kod1c], one=True)
	query = "INSERT INTO "+department000+" (kod1c,sk,qty,idDep,timecreate) VALUES('"+kod1c+"','"+sk+"',"+qty+","+str(currentDepId)+",'"+str(datetime.datetime.now())+"')"

	con = lite.connect(DATABASE)
	with con:
		cur = con.cursor()    
		cur.execute(query)

	with con:
		cur = con.cursor()    
		cur.execute("SELECT last_insert_rowid()")
		idRow = cur.fetchall()
	
	updateDep000(department000,currentDepId)
	
	return str(idRow[0][0])

def updateDep000(department000,currentDepId):	
	con = lite.connect(DATABASE)
	curD = con.cursor()
	curD.execute("UPDATE departments SET counts = (select count(*) from "+department000+" where qty <> 0) where id = "+str(currentDepId))
	con.commit()
	con.close()
		
@app.route('/newItem')
def newItem():
	return render_template("newItem.html",sk=request.args.get('sk'),idDep=request.args.get('idDep'))
	
@app.route('/addNewItem', methods=['POST'])
def addNewItem():
	data = request.get_json()
	sk = data['sk']
	name = data['itemName']
	idDep = data['idDep']
	if sk == None:
		return ""
		
	con = lite.connect(DATABASE)
	try:
		cur = con.cursor()
		query = "INSERT INTO goods (kod1c,name,sk,timecreate) VALUES('NewItem','"+name+"','"+sk+"','"+str(datetime.datetime.now())+"')"
		cur.execute(query)
		con.commit()
		
		cur.execute("SELECT last_insert_rowid()")
		con.commit()
		idRow = str(cur.fetchall()[0][0])

		query = "UPDATE goods set kod1c = '"+str(idDep) + "NEW"+idRow + "' where rowid = " + idRow
		print(query)
		cur.execute(query)
		con.commit()
	except:
		print("Unexpected error: "+ str(sys.exc_info()[0]))
		
	cur.close()
	con.close()
	
	return ""
	


@app.route('/foundit')
def foundit():
	curDep = getCurrentDepartment()
	if curDep is None:
		#currentDepId = 0
		#departmentName = "It should choose department!!!"
		return redirect(url_for('departments'))
	else:
		currentDepId = curDep[0]
		departmentName = curDep[1]

	department000 = "department"+str(currentDepId);

	sku = request.args.get('sku', default = '', type = str)

	# chose SKU from goods
	query = "SELECT * FROM goods gg where gg.sk = ?"
	isGood = query_db(query,[sku],one=True)
	if isGood == None:
		return redirect(url_for('newItem',sk=sku,idDep=currentDepId))
	else:
		result = [isGood]
	print(result)	
		
	con = lite.connect(DATABASE)
	# chose only last one	
	with con:
		curF = con.cursor()    
		curF.execute("SELECT id,qty FROM "+department000+" where sk = '"+sku+"' ORDER BY timecreate DESC LIMIT 1")
		rvF = curF.fetchall()
		try:
			idRow = rvF[0][0]
			qty = rvF[0][1]
		except:
			idRow = 0
			qty = 0

	curT = con.cursor()
	curT.execute("SELECT gg.kod1c, gg.sk, gg.name, d.qty, d.timecreate as timecreate, ds.name as dname, d.id as id \
				  FROM goods gg,"+department000+" d,departments ds \
				  where ds.id = "+str(currentDepId)+" and gg.sk = d.sk \
				  ORDER BY timecreate DESC");
	rvT = curT.fetchall()
	table = rvT
		
	param = (0,currentDepId,departmentName,qty,sku,idRow)

	return render_template("foundit.html",result=result,table=table, param=param)
	
	
@app.route('/deps')
def departments():
	curDep = getCurrentDepartment()
	if curDep is None:
		currentDepId = 0
		departmentName = "Please choose department !!!"
		depIdChosen = False
	else:
		currentDepId = curDep[0]
		departmentName = curDep[1]
		depIdChosen = True
	
	if (currentDepId==0):
		depIdChosen = False

	dep = (depIdChosen, currentDepId)
	
	con = lite.connect(DATABASE)
	with con:
		cur = con.cursor()    
		cur.execute("SELECT id, name, counts FROM departments")
		rv = cur.fetchall()
		result = rv
	
	return render_template("departments.html",result=result,dep=dep)

# Change department
@app.route('/changeDep', methods=['POST'])
def changeDep():
	data = request.get_json()
	newDepId = data['newDepId']

	con = lite.connect(DATABASE)
	with con:
		cur = con.cursor()    
		cur.execute("UPDATE constants SET valueInt = "+newDepId+" where name = 'Department'")
	return ""
		
# Upload to local MySQL
@app.route('/upload', methods=['POST'])
def upload():
	data = request.get_json()
	idDep = data['idDep']
	department000 = "department"+str(idDep)

	con = lite.connect(DATABASE)
	cursor = con.cursor()
	# 1 - Start Dump/Upload to server
	query = "UPDATE constants set valueInt = 1 where name = 'StartDump'"
	cursor.execute(query)
	con.commit()
		
	try:
		print('1')
		# 2.1 choose data from department000
		query = "select kod1c, sum(qty) from " + department000 + " group by kod1c"
		print(query)
		rowq = query_db(query, (), one=False)
		
		print('2')
		# 2.2 connect to MySQL DB
		conMy = mysql.connector.connect(user='sql11206944', password='McQ4scpNVX',
								  host='sql11.freemysqlhosting.net',
								  database='sql11206944')
		cursorMy = conMy.cursor()
		
		print('3')
		# 2.3 fill temp with 1
		query = "UPDATE gerasymchuk_store set temp = 1 where idDep = "+idDep
		cursorMy.execute(query)
		conMy.commit()
		
		print('4')
		# 2.4 fill MySQL DB with data
		for line in rowq:
			idDepKod1c = str(int(idDep)*100)+line[0]
			query = "INSERT INTO gerasymchuk_store (id,kod1c,idDep,qty,temp) VALUES(%s,%s,%s,%s,2) \
			ON DUPLICATE KEY UPDATE qty = %s, temp = 2"
			cursorMy.execute(query, (idDepKod1c, line[0], idDep, line[1], line[1]))
			conMy.commit()
			
		# print('5')
		# 3 delete all where temp <> 2
		query = "delete from gerasymchuk_store where temp <> 2 and idDep = "+idDep
		cursorMy.execute(query)
		conMy.commit()

		# print('6')
		# 4 chage temp = 0
		query = "UPDATE gerasymchuk_store set temp = 0 where idDep = "+idDep
		cursorMy.execute(query)
		conMy.commit()

		# print('7')
		query = "UPDATE constants set valueInt = 0 where name = 'StartDump'"
		cursor.execute(query)
		con.commit()

		# print('8')
		# finally
		con.close()
		conMy.close()

		# flash("Uload OK")
		# print("flash")
		print("Done");
		return "Done"
	except:
		print("Unexpected error: ", sys.exc_info()[0])
		print("Not done");
		return "Not done"
		
		
@app.route('/searchforcod')
def searchforcod():
	return render_template("searchforcod.html")


	
@app.route('/mysql')
def mysql12():
	cnx = mysql.connector.connect(user='sql11206944', password='McQ4scpNVX',
                              host='sql11.freemysqlhosting.net',
                              database='sql11206944')
	cnx.close()
	
	return 'It looks connected'

'''
	#	cur = mysql.connection.cursor()
	db=MySQLdb.connect(host="sql11.freemysqlhosting.net",user="sql11206944",passwd="McQ4scpNVX",db="sql11206944")
	cur = db.cursor()
	cur.execute("SELECT * FROM example1_dishes")

	#cur.execute(SELECT id, name FROM example1_dishes)
	#row_headers=[x[0] for x in cur.description] #this will extract row headers

	rv = cur.fetchall()
	db.close
	
	json_data=[]
	for result in rv:
		json_data.append(dict(zip(row_headers,result)))
	res1 = json.dumps(json_data)
	result = json.loads(res1)

	result = rv
	return render_template('jquery2.html',result = result)
'''

@app.route('/result')
def result():
   dict = {'14':'Borshch','22':'Varenyky','321':'Uzvar'}
   return render_template('result.html', result = dict)
   
@app.route('/table')
def table():
	dict = {'14':'Borshch','22':'Varenyky','321':'Uzvar'}
	return render_template("jquery2.html",result=dict)

@app.route('/profile/<name>')
def profile(name):
	namePar = "aaaaa"
	return render_template("profile.html",name=name)

@app.route('/')
def index():
	sku = request.args.get('sku', default = '', type = str)
	return "<b>Hello</b> it's me. It is home %s" % sku

@app.route('/about')
def about():
	return "<b>About</b>"

@app.route('/post/<int:post_id>')
def post_id(post_id):
	return "<b>post id is %s</b>" % post_id

@app.route('/method',methods=['GET','POST'])
def method():
	if request.method == 'POST':
		return "POST"
	else:
		return "GET"

	
if __name__ == "__main__":
	app.run(host='0.0.0.0')