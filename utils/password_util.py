import bcrypt

class PasswordUtil:

    @staticmethod
    def hash_password(raw_password: str) -> str:

        if not raw_password or len(raw_password) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres.") 
        

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(raw_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))
    

