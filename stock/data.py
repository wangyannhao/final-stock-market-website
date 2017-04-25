import sqlite3
 
def read_from_db():
	c.execute('SELECT *FROM alldata')
	data=c.fetchall()
	return(data)

conn=sqlite3.connect('nepsedata.sqlite3') 
c=conn.cursor()
n_d=read_from_db()

bank_data=[]
devbank_data=[]
finance_data=[]
hotel_data=[]
hydropower_data=[]
insurance_data=[]
nepse_data=[]
others_data=[]

for i in n_d:
	bank_data.append(i[0])
	devbank_data.append(i[1])
	finance_data.append(i[2])
	hotel_data.append(i[3])
	hydropower_data.append(i[4])
	insurance_data.append(i[5])
	nepse_data.append(i[6])
	others_data.append(i[7])
	


