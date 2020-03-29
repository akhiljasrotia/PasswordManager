import hashlib
import os
from base64 import b64encode

users = {} # A simple demo storage

# Add a user
username = 'Brent' # The users username
password = 'mypassword' # The users password

salt = os.urandom(32) # A new salt for this user
'''
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
users[username] = { # Store the salt and key
    'salt': salt,
    'key': key
}'''

#st1 = salt.decode('utf-8','strict')
token = salt.decode('base-64')

print("The actual salt is ",salt)
print("The salt is ",token)


#token1 = token.decode('utf-8')
#print(token1)



##	print("YES")
#print("The kEY is",key)