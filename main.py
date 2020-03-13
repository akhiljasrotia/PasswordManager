import mysql.connector


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
#mycursor.execute("CREATE TABLE users (Username VARCHAR(255),Password VARCHAR(255))")

userNames = []


#Code to check if the user is valid or not
def authenticate():
	uname = input("Enter your registered Username: ")
	pword = input("Enter your master password: ")
	sql = "SELECT * FROM users WHERE Username = %s and Password = %s"
	data = (uname,pword)
	mycursor.execute(sql,data)
	myresult = mycursor.fetchall()
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


#Code to create the username and super password 
def createUser():
	user = input("Enter your Username: ")
	password = input("Enter your Super Password: ")
	sql = "INSERT INTO users (Username,Password) VALUES (%s, %s)"
	val = (user,password)
	mycursor.execute(sql, val)
	mydb.commit()
	main()	#Calling the main function again



#Code to add password in the password manager
def addPassword():
	exist = authenticate()
	if(exist):
		userName = input("Enter your Username: ")
		application = input("Enter the Application Name: ")
		pword = input("Enter the Password: ")
		sql = "INSERT INTO customers (Username,Application,Password) VALUES (%s, %s ,%s)"
		val = (userName, application,pword)
		mycursor.execute(sql, val)
		mydb.commit()
	else:
		print("No such User exists")
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
	print("Enter your preference \n")
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