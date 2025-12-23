from config.connection import db_connection

class UsuariosSistemaRepository:
    
    def __init__(self, conn_factory = db_connection):
        self.conn_factory = conn_factory

    #/////////////////////////
    #CRUD Basico
    #/////////////////////////

    def create(self, username, password, id_permissao, id_funcionario = None):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO usuarios_sistema (id_funcionario, username, password, id_permissao)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
        """

        cur.execute(query, (id_funcionario, username, password, id_permissao))
        id_usuarios_sistema = cur.fetchone()[0]

        cur.close()
        conn.close()
        return id_usuarios_sistema
    
    def get_by_id(self, id_usuarios_sistema):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, username, password, id_permissao FROM usuarios_sistema
                WHERE id = (%s);
        """

        cur.execute(query, (id_usuarios_sistema,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "id_funcionario" : row[1],
                "username" : row[2],
                "password" : row[3],
                "id_permissao" : row[4]
            }

        return None

    def get_all(self):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, username, password, id_permissao FROM usuarios_sistema;
        """

        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "id_funcionario": r[1], "username" : r[2], "password" : r[3], "id_permissao" : r[4] }
            for r in rows
        ]

    def update(self,  id_usuarios_sistema, id_funcionario = None, username = None, password = None, id_permissao = None ):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        fields = []
        values = []
        
        if id_funcionario is not None:

            fields.append("id_funcionario = %s")
            values.append(id_funcionario)

        if password is not None:

            fields.append("password = %s")
            values.append(password)
        
        if username is not None:

            fields.append("username = %s")
            values.append(username)

        if id_permissao is not None:

            fields.append("id_permissao = %s")
            values.append(id_permissao)

        if not fields:
            
            cur.close()
            conn.close()
            return False

        query = f"""
                UPDATE usuarios_sistema
                SET {','.join(fields) }
                WHERE id = %s;
        """

        values.append(id_usuarios_sistema)
        cur.execute(query, values)

        cur.close()
        conn.close()
        return True


    def delete(self, id_usuarios_sistema):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                DELETE FROM usuarios_sistema
                WHERE id = %s;
        """

        cur.execute(query, (id_usuarios_sistema,))

        cur.close()
        conn.close()
        return id_usuarios_sistema
    
    #/////////////////////////
    #Métodos adicionais
    #/////////////////////////



    def get_by_username(self, username):
        conn = self.conn_factory()

        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, username, password, id_permissao FROM usuarios_sistema
                WHERE username ILIKE %s;
        """

        cur.execute(query, (username,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "id_funcionario" : row[1],
                "username" : row[2],
                "password" : row[3],
                "id_permissao" : row[4]
            }

        return None
    
    def get_by_funcionario_id(self, id_funcionario):
        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, username, password, id_permissao FROM usuarios_sistema
                WHERE id_funcionario = %s;
        """

        cur.execute(query, (id_funcionario,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "id_funcionario" : row[1],
                "username" : row[2],
                "password" : row[3],
                "id_permissao" : row[4]
            }

        return None
    
    def delete_by_funcionario_id(self, id_funcionario):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                DELETE FROM usuarios_sistema
                WHERE id_funcionario = %s;
        """

        cur.execute(query, (id_funcionario,))

        cur.close()
        conn.close()
        return True