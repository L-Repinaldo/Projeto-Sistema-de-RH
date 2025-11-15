
class UsuariosSistemaRepository():
    
    def __init__(self, conn_factory):
        self.conn_factory = conn_factory

    def create(self, username, password, role, id_funcionario = None):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO usuarios_sistema (id_funcionario, username, password, role)
                VALUES (%s, %s, %s)
                RETURNING id;
        """

        cur.execute(query, (id_funcionario, username, password, role))
        id_usuarios_sistema = cur.fetchone()[0]

        cur.close()
        conn.close()
        return id_usuarios_sistema
    
    def get_by_id(self, id_usuarios_sistema):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario FROM usuarios_sistema
                WHERE id = (%s);
        """

        cur.execute(query, (id_usuarios_sistema))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "id_funcionario" : row[1],
                "username" : row[2],
                "password" : row[3],
                "role" : row[4]
            }

        return None

    def get_all(self):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, username, password, role FROM usuarios_sistema;
        """

        cur.execute(query)
        rows = cur.fetchall

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "id_funcionario": r[1], "username" : r[2], "password" : r[3], "role" : r[4] }
            for r in rows
        ]

    def update(self,  id_usuarios_sistema, id_funcionario = None, username = None, password = None, role = None ):

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

        if role is not None:

            fields.append("role = %s")
            values.append(role)

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

        cur.execute(query, (id_usuarios_sistema))

        cur.close()
        conn.close()
        return id_usuarios_sistema
