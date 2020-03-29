#For connecting to Mysql database
import mysql.connector
#For hashing functions
import hashlib
#For creating Salt
import os



#Connection to MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="dragon ball",
  database="PassMan"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE PassMan")
#mycursor.execute("CREATE TABLE customers (Username VARCHAR(255),Application VARCHAR(255),Password VARCHAR(255))")
#mycursor.execute("CREATE TABLE salt (Username VARCHAR(255),Salt nvarchar(255))")
#mycursor.execute("CREATE TABLE users (Username VARCHAR(255),Password VARCHAR(255))")


userNames = []
existing_users = [] #To check whether user already exists or not

def create_salt():
	#Generating Salt to add with the hashed password
	salt = os.urandom(32)
	return salt

def hashing_passwords(password,salt):
	#Generating the hashed key which contains salt and UTF-8 version of password
	#print(password)
	key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
	return key


#Code to check if the user is valid or not
def authenticate():
	uname = input("Enter your registered Username: ")
	pword = input("Enter your master password: ")
	sql = "SELECT * FROM salt WHERE Username = %s"
	#data = (uname)
	mycursor.execute(sql,(uname,))
	myresult = mycursor.fetchall()
	for each in myresult:
		salt1=each[1]

	print(salt1)
	get_hashed_pwd = hashing_passwords(pword,salt1)
	print(get_hashed_pwd)
	if myresult:
		return True
	else:
		return False
	

#Code to see all the users present in the password manager
def viewUsers():
	sql = "SELECT * FROM users"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	if(myresult):
		print("\n \n")
		print("The users registered are: ")
		for each in myresult:
			print(each[0])
	else:
		print("No users are registered ")
	main()	#Calling the main function again


#Code to check the existing users while creating a new user:
def check_existing_users():
	sql = "SELECT * FROM Salt"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	for each in myresult:
		existing_users.append(each[0])

#Code to create the username and super password 
def createUser():
	user = input("Enter your Username: ")
	check_existing_users() #Bring all presently stored usernames
	#print(existing_users)
	if user in existing_users:
		print("Username already exists , choose a different username")
		createUser()
	else:
		password = input("Enter your Super Password: ")
		salt1 = create_salt()
		sql1 = "INSERT INTO salt (Username,Salt) VALUES (%s, %s)"
		val1 = (user,salt1)
		mycursor.execute(sql1,val1)
		#mydb.commit()
		npass = str(hashing_passwords(password, salt1))
		print(npass)
		sql = "INSERT INTO users (Username,Password) VALUES (%s, %s)"
		val = (user,npass)
		mycursor.execute(sql, val)
		mydb.commit()
		main()	#Calling the main function again



#Code to add password in the password manager
def addPassword():
	#exist = 
	authenticate()
	if(exist):
		userName = input("Enter your Username: ")
		application = input("Enter the Application Name: ")
		pword = input("Enter the Password: ")
		sql = "INSERT INTO customers (Username,Application,Password) VALUES (%s, %s ,%s)"
		val = (userName, application,pword)
		mycursor.execute(sql, val)
		mydb.commit()
	else:
		print("The credentials are wrong or you haven't registered yet")
	main()	#Calling the main function again
	#print("Your userName is ",userName)
	


#Code to view stored password
def viewPassword():
	exist = authenticate()
	if(exist):
		print("\n \n")
		uName = input("Enter your stored Username: ")
		application = input("Enter the Application Name: ") 
		sql = "SELECT * FROM customers WHERE Username = %s and Application = %s"
		data = (uName,application)
		mycursor.execute(sql,data)
		myresult = mycursor.fetchall()

		tempListPassword = []
		tempListApp = []

		for each in myresult:
			tempListPassword.append(each[2])
			tempListApp.append(each[1])

		print("\n \n")
		print("The password for ",tempListApp[0],"is: ",tempListPassword[0])
	else:
		print("No such User exists")
	main()	#Calling the main function again

def exit():	
	print("Thanks for using PassMan!")
	quit()


def functions_mapper(choice):
	switcher = {
		1:createUser,
		2:viewUsers,
		3:addPassword,
		4:viewPassword,
		5:exit,
	}
	
	func = switcher.get(choice, lambda: "Invalid Number")
	func()



#Main driver function
def main():
	print("\n \n")
	print("Enter your preference: \n")
	print("1 to Create User")
	print("2 to View users")
	print("3 for Add Password")
	print("4 for View Password")
	print("5 to Exit \n")


	choice = int(input())
	functions_mapper(choice)


#Calling the main function
if __name__ == "__main__":
	print("Welcome to PassMan , you can store , generate and retrieve your passwords here")
	main()