from model.user import User
import api.connectionRepository as con

class AuthRepository:       
    def authenticate(self, user: User) -> User | None:
        db = con.ConnectionRepository().connexionDatabase()
        try:
            cursor = db.cursor()
            query = """
                SELECT id, name, user, password
                FROM users 
                WHERE user = ? AND password = ?
            """
            cursor.execute(query, (user._user, user._password))
            row = cursor.fetchone()
            
            if row:
                return User(name=row[1], user=row[2])
        except Exception as e:

            print("Error durante la autenticación:", e)
        finally:
            db.close()
        
        return None