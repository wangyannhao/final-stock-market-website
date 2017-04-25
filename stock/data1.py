import sqlite3

conn = sqlite3.connect('nepse_only.sqlite3')
c = conn.cursor()  
def read_form_db():
	c.execute('SELECT * FROM alldata')    
	data=c.fetchall()
	return (data)
list_data = read_form_db()
list_data.reverse()

neps_data=[]
for i in list_data:
	neps_data.append(i[0])

#

print(neps_data)