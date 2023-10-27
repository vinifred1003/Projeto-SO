from model.DatabaseConnection import DatabaseConnection

class UsersModel:
    def __init__(self):
        conecction = DatabaseConnection()
        self.cursor = conecction.getCursor()
        
    def create(self, name, password):
        if not name or not password:
            raise Exception("Faltando dados obrigatórios")
    
        user_exists = self.getUserByName(name)
        if user_exists:
            raise Exception("Usuário já existente")

        self.cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
        self.cursor.connection.commit()
        
        user_id = self.cursor.lastrowid
        
        return user_id
            
    def authenticate(self, user_name , password):
        self.cursor.execute("SELECT * FROM users WHERE name=? ", (user_name,))
        result = self.cursor.fetchone()
        
        if not result:
            raise Exception("Usuário não encontrado")
        dataBaseUser = {
            "uid": result[0],
            "name": result[1],
            "password": result[2],
        }
        
        if dataBaseUser["password"] != password:
            raise Exception("Senha inválida")
        
        return {"uid": dataBaseUser["uid"]}

    def getUserByUid(self, user_uid):
        self.cursor.execute("SELECT * FROM users WHERE uid=?", (int(user_uid), ))
        dataBaseUser = self.cursor.fetchone()
        return (dataBaseUser)

    def getUserByName(self, name):
        self.cursor.execute("SELECT * FROM users WHERE uid=?", (name, ))
        dataBaseUser = self.cursor.fetchone()
        return (dataBaseUser)
    
    
    
usersModel = UsersModel()