import security

password = input("entrer le mot de passe :")

print(security.get_password_hash(password))

