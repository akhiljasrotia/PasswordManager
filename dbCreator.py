import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  #Uncomment this line after creating the DB
  #database="PassMan"
)

mycursor = mydb.cursor()


#Run this first and then comment it 
mycursor.execute("CREATE DATABASE PassMan")

#Uncomment the below lines after creating the Db

'''
mycursor.execute("CREATE TABLE customers (	MasterUsername VARCHAR(255),Username VARCHAR(255),Application VARCHAR(255),Password VARCHAR(255))")
mycursor.execute("CREATE TABLE salt (Username VARCHAR(255),Salt nvarchar(255))")
mycursor.execute("CREATE TABLE users (Username VARCHAR(255),Password VARCHAR(255))")
'''