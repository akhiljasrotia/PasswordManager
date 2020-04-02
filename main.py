import mysql.connector #For connecting to Mysql database
import hashlib #For hashing functions
import os #For creating Salt
import getpass #For hiding user input
import pyperclip #For Copying the generated password
import random





#Connection to MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="PassMan"
)

mycursor = mydb.cursor()

#def initiateDB():
	#mycursor.execute("CREATE DATABASE PassMan")
	#mycursor.execute("CREATE TABLE customers (	MasterUsername VARCHAR(255),Username VARCHAR(255),Application VARCHAR(255),Password VARCHAR(255))")
	#mycursor.execute("CREATE TABLE salt (Username VARCHAR(255),Salt nvarchar(255))")
	#mycursor.execute("CREATE TABLE users (Username VARCHAR(255),Password VARCHAR(255))")


userNames = []
existing_users = [] #To check whether user already exists or not
existing_apps = []

def create_salt():
	#Generating Salt to add with the hashed password
	salt = os.urandom(32)
	return salt

def hashing_passwords(password,salt):
	#Generating the hashed key which contains salt and UTF-8 version of password
	key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
	return key

#Runner for logged in user
def loggedIn(user):
	print("\n\nEnter your preference: \n")
	print("1 to Store Credentials")
	print("2 to View Credentials")
	print("3 to View Apps")
	print("4 to Modify stored Credentials")
	print("5 to Edit profile")
	print("6 to Log out\n")

	choice = int(input())
	login_functions_mapper(choice,user)

#Code to check if the user is valid or not
def authenticate():
	uname = input("Enter your Master Username: ")
	check_existing_users()
	if uname.lower() in existing_users:
		pword = getpass.getpass("Enter your Master Password: ")
		sql = "SELECT * FROM salt WHERE Username = %s"
		mycursor.execute(sql,(uname,))
		myresult = mycursor.fetchall()
		for each in myresult:
			salt1=each[1]

		get_hashed_pwd = hashing_passwords(pword,eval(salt1)) #Hashing the entered password with the original salt
		sql1 = "SELECT * FROM users WHERE Username = %s"
		mycursor.execute(sql1,(uname,))
		myresult1 = mycursor.fetchall()
		for each in myresult1:
			pwd1=each[1]

		if str(pwd1)==str(get_hashed_pwd): #Checking if the hashed passwords are matching
			print("\nLogged In successfully as",uname,"\n")	
			loggedIn(uname)

		else:
			print("\nPassword entered is incorrect")
			authenticate()
	else:
		print("User doesn't exist")
		main()
	

#Code to see all the users present in the password manager
def viewUsers():
	sql = "SELECT * FROM users"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	if(myresult):
		print("\n")
		print("The users registered are: \n")
		i=1
		for each in myresult:
			print('%d) %s' %(i,each[0]))
			i+=1
	else:
		print("No users are registered ")
	main()	#Calling the main function again


#Code to check the existing users while creating a new user:
def check_existing_users():
	sql = "SELECT * FROM Salt"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	for each in myresult:
		existing_users.append(each[0].lower())

#Code to create the username and super password 
def createUser():
	user = input("Enter your PassMan Username: ")
	check_existing_users() #Bring all presently stored usernames
	#print(existing_users)
	if user.lower() in existing_users:
		print("\n \n")
		print("Username already exists , choose a different username \n")
		createUser()
	else:
		password = getpass.getpass("Enter your Super Password(You need to remember this to log in): ")
		password1 = getpass.getpass("Re-Enter your password: ")
		if(password==password1):
			salt1 = create_salt()
			sql1 = "INSERT INTO salt (Username,Salt) VALUES (%s, %s)"
			val1 = (user,str(salt1))
			mycursor.execute(sql1,val1)
			#mydb.commit()
			npass = str(hashing_passwords(password, salt1))
			#print(npass)
			sql = "INSERT INTO users (Username,Password) VALUES (%s, %s)"
			val = (user,npass)
			mycursor.execute(sql, val)
			mydb.commit()
			print("\n \n")
			print("User account has been created successfully \n")
			print("Do you want to log in now?")
			print("1 to LogIn now")
			print("2 to Cancel\n")

			loginchoice = int(input())
			if(loginchoice==1):
				print("\nLogged In successfully as",user,"\n")	
				loggedIn(user)
			else:
				main()
		else:
			print("\nPasswords didn't match\n")
			createUser()
		main()	#Calling the main function again



#Code to add password in the password manager
def addPassword(user):
	exist = user
	check_application_exists(exist,"application")
	print("\nThe already stored apps by",exist,"are: ")
	for i in range(0,len(existing_apps)):
		print('%d)%s'% (i+1,existing_apps[i]))
	application = input("\nEnter the App Name: ")
	exist_app = check_application_exists(exist, application)
	if not exist_app:
		userName = input("Enter your App Username: ")
		pword = getpass.getpass("Enter the App Password: ")
		pword1 = getpass.getpass("Re-Enter the App Password: ")
		if(pword==pword1):
			sql = "INSERT INTO customers (MasterUsername,Username,Application,Password) VALUES (%s,%s,%s,%s)"
			val = (exist,userName, application,pword)
			mycursor.execute(sql, val)
			mydb.commit()
			print("\nYour password and username for",application,"has been stored \n")
		else:
			print("\nThe passwords didn't match")
	else:
		print("\nThe app credentials are already present in the database")
	loggedIn(exist)	
	


#Code to see if application for the user exists or not
def check_application_exists(username,application):
	sql = "SELECT application FROM customers WHERE MasterUsername = %s"
	mycursor.execute(sql,(username,))
	myresult = mycursor.fetchall()
	existing_apps.clear()
	tempAppList = []
	for each in myresult:
		tempAppList.append(each[0].lower())
		existing_apps.append(each[0])

	if application.lower() in tempAppList:
		return True
	else:
		return False

#Code to view stored password
def viewPassword(user):
	exist = user #Exist is being used as MasterUsername
	check_application_exists(exist,"application")
	print("\nThe apps stored by",exist,"are: ")
	for i in range(0,len(existing_apps)):
		print('%d)%s'% (i+1,existing_apps[i]))
	application = input("\nEnter the App Name: ") 

	app_exists = check_application_exists(exist,application)

	if(app_exists):
		sql = "SELECT * FROM customers WHERE MasterUsername=%s and Application = %s"
		data = (exist,application)
		mycursor.execute(sql,data)
		myresult = mycursor.fetchall()

		tempListPassword = []
		tempListUsername = []

		for each in myresult:
			tempListPassword.append(each[3])
			tempListUsername.append(each[1])

		print("The username for",application,"is: ",tempListUsername[0])
		print("The password for",application,"is: ",tempListPassword[0])
	else:
		print("\n")
		print("No password is stored for",application)
	loggedIn(exist)	

#Code for modifying master user
def modifyMasterUser(user):
	print("\nEnter your preference: \n")
	print("1 to Delete User")
	print("2 to Modify User")
	print("3 to Cancel\n")

	choice = int(input())
	print("\n")

	#Deleting the Master user will delete all the passwords stored by that user
	if(choice==1):
		user = user

		pword = getpass.getpass("Enter your Master Password: ")
		sqlx = "SELECT * FROM salt WHERE Username = %s"
		mycursor.execute(sqlx,(user,))
		myresult = mycursor.fetchall()
		for each in myresult:
			salt1=each[1]

		get_hashed_pwd = hashing_passwords(pword,eval(salt1))
		sqlx1 = "SELECT * FROM users WHERE Username = %s"
		mycursor.execute(sqlx1,(user,))
		myresult1 = mycursor.fetchall()
		for each in myresult1:
			pwd1=each[1]

		if str(pwd1)==str(get_hashed_pwd):
			sql = "DELETE FROM customers WHERE MasterUsername=%s"
			mycursor.execute(sql,(user,))
			sql1 = "DELETE FROM users WHERE Username=%s"
			mycursor.execute(sql1,(user,))
			sql2 = "DELETE FROM salt WHERE Username=%s"
			mycursor.execute(sql2,(user,))
			mydb.commit()

			print("\nThe user and the credentials have been deleted")
			main()
		else:
			print("\n Password is wrong ,try again \n")
			loggedIn(user)

	elif(choice==2):
		print("Enter 1 to change Username")
		print("Enter 2 to change Password")
		print("Enter 3 to cancel\n")
		choice1 = int(input())

		if(choice1==1):
			user = user
			newUser = input("Enter the New Username: ")
			check_existing_users()
			if newUser.lower() not in existing_users:
				sql = "UPDATE users SET Username = %s where Username = %s"
				mycursor.execute(sql,(newUser,user,))
				sql1 = "UPDATE salt SET Username = %s where Username = %s"
				mycursor.execute(sql1,(newUser,user,))
				sql2 = "UPDATE customers SET MasterUsername = %s where MasterUsername = %s"
				mycursor.execute(sql2,(newUser,user,))
				mydb.commit()

				print("\nThe username has been updated")
				loggedIn(newUser)
			else:
				print("\nThe username already exists")
				modifyMasterUser(user)
		elif(choice1==2):
			user = user
			newPass = getpass.getpass("Enter the New Password: ")
			newPass1 = getpass.getpass("Re-Enter the Password: ")
			if(newPass==newPass1):
				sql = "SELECT * FROM salt WHERE Username = %s"
				mycursor.execute(sql,(user,))
				myresult = mycursor.fetchall()
				for each in myresult:
					salt1=each[1]

				newPwd = str(hashing_passwords(newPass,eval(salt1)))
				sql1 = "UPDATE users SET Password = %s where Username = %s"
				mycursor.execute(sql1,(newPwd,user,))
				mydb.commit()

				print("\nThe password has been changed successfully")
			else:
				print("\nThe passwords didn't match")
				modifyMasterUser(user)
		elif(choice1==3):
			pass
		else:
			print("\nInvalid request \n")		
	else:
		pass
	loggedIn(user)	

#Code to see the stored app 
def viewApps(user):
	exist = user
	check_application_exists(exist,"application")
	print("\nThe apps stored by",exist,"are: ")
	for i in range(0,len(existing_apps)):
		print('%d)%s'% (i+1,existing_apps[i]))
	loggedIn(user)


#Code to modify stored credentials
def modifyStoredCredentials(user):
	print("\nEnter your preference: \n")
	print("1 to Delete App credentials")
	print("2 to Modify App credentials")
	print("3 to Cancel\n")

	choice = int(input())
	print("\n")

	if(choice==1):
		exist=user
		check_application_exists(exist,"application")
		print("\nThe apps stored by",exist,"are: ")
		for i in range(0,len(existing_apps)):
			print('%d)%s'% (i+1,existing_apps[i]))
		
		appTBD = input("\nEnter the App name:")
		exist1 = check_application_exists(exist,appTBD)
		if(exist1):
			sql = "DELETE FROM customers WHERE MasterUsername=%s and Application=%s"
			mycursor.execute(sql,(exist,appTBD,))
			mydb.commit()
			print("\nCredentials for",appTBD,"have been deleted")
		else:
			print("\nCredentials for",appTBD,"are not present in the database")
			modifyStoredCredentials(user)

	elif(choice==2):
		exist=user
		check_application_exists(exist,"application")
		print("\nThe apps stored by",exist,"are: ")
		for i in range(0,len(existing_apps)):
			print('%d)%s'% (i+1,existing_apps[i]))

		print("\nEnter your preference: ")
		print("1 to Change App Name")
		print("2 to Change Username")
		print("3 to Change Password")
		print("4 to cancel\n")

		choice1 = int(input())

		if(choice1==1):
			app1 = input("\nEnter the app name: ")
			exist1 = check_application_exists(exist,app1)
			if(exist1):
				newApp = input("\nEnter the new app name: ")
				exist2 = check_application_exists(exist,newApp)

				if not exist2:
					sql1 = "UPDATE customers SET Application = %s where MasterUsername = %s and Application = %s"
					mycursor.execute(sql1,(newApp,exist,app1))
					mydb.commit()
					print("\nThe name has been changed successfully")
				else:
					print("\nThe name already exists , choose a different name")
					modifyStoredCredentials(user)
			else:
				print("\nCredentials for",app1,"are not present in the database")
				modifyStoredCredentials(user)
		elif(choice1==2):
			app1 = input("\nEnter the app name: ")
			exist1 = check_application_exists(exist,app1)
			if(exist1):
				newUser = input("\nEnter the new username: ")
				sql1 = "UPDATE customers SET username = %s where MasterUsername = %s and Application = %s"
				mycursor.execute(sql1,(newUser,exist,app1))
				mydb.commit()
				print("\nThe Username has been changed successfully")
			else:
				print("\nCredentials for",app1,"are not present in the database")
				modifyStoredCredentials(user)
		elif(choice1==3):
			app1 = input("\nEnter the app name: ")
			exist1 = check_application_exists(exist,app1)
			if(exist1):
				newPass = getpass.getpass("\nEnter the new password: ")
				newPass1 = getpass.getpass("Re-Enter the password: ")
				if(newPass==newPass1):
					sql1 = "UPDATE customers SET Password = %s where MasterUsername = %s and Application = %s"
					mycursor.execute(sql1,(newPass,exist,app1))
					mydb.commit()
					print("\nThe password has been changed successfully")
				else:
					print("\nThe passwords didn't match")
					modifyStoredCredentials(user)
			else:
				print("\nCredentials for",app1,"are not present in the database")
				modifyStoredCredentials(user)
	loggedIn(user)


#Code to generate a random password 
def generatePassword():
	s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
	print("\nEnter the desired length of the password(min 8 characters): ")
	passlen = int(input())
	if(passlen>=8):
		pword =  "".join(random.sample(s,passlen ))
		print("Randomly generated password is: ",pword)
		print("\nDo you want to copy the generated password to the clipboard? ")
		print("Enter your preference:\n")
		print("1 to copy")
		print("2 to cancel")
		choice = int(input())
		if(choice==1):
			pyperclip.copy(pword)
		else:
			main()

	else:
		print("\nMinimum length is 8")
		generatePassword()
	main()

def logout(user):
	print("\n")
	print(user,"is logged out!")
	main()

#Code to exit the application
def exit():	
	print("Thanks for using PassMan!")
	quit()


def login_functions_mapper(choice,user):
	switcher = {
		1:addPassword,
		2:viewPassword,
		3:viewApps,
		4:modifyStoredCredentials,
		5:modifyMasterUser,
		6:logout
	}
	
	func = switcher.get(choice, lambda: "Invalid Choice")
	func(user)



def functions_mapper(choice):
	switcher = {
		1:createUser,
		2:authenticate,
		3:viewUsers,
		4:generatePassword,
		5:exit,
	}
	
	func = switcher.get(choice, lambda: "Invalid Choice")
	func()



#Main driver function
def main():
	print("\n")
	print("Enter your preference: \n")
	print("1 to SignUp")
	print("2 to LogIn")
	print("3 to View Users")
	print("4 to Generate Password")
	print("5 to Exit \n")


	choice = int(input())
	functions_mapper(choice)


#Calling the main function
if __name__ == "__main__":
	print("Welcome to PassMan! , you can store , delete , generate and retrieve your passwords here")
	main()