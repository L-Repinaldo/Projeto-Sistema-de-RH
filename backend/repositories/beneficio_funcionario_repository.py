from config.connection import db_connection

class BeneficioFuncionarioRepository:
    
    def __init__(self, conn_factory = db_connection):
        self.conn_factory = conn_factory


    #/////////////////////////
    #CRUD Basico
    #/////////////////////////

    def create(self, id_funcionario, id_beneficio, ativo):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO beneficio_funcionario (id_funcionario, id_beneficio, ativo)
                VALUES (%s, %s, %s)
                RETURNING id;
        """

        cur.execute(query, (id_funcionario, id_beneficio, ativo))
        id_beneficio_funcionario = cur.fetchone()[0]

        cur.close()
        conn.close()
        return id_beneficio_funcionario
    
    def get_by_id(self, id_beneficio_funcionario):

        conn = self.conn_factory()

        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, id_beneficio, ativo FROM beneficio_funcionario
                WHERE id = %s;
        """

        cur.execute(query, (id_beneficio_funcionario,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "id_funcionario" : row[1],
                "id_beneficio" : row[2],
                "ativo" : row[3]
            }

        return None

    def get_all(self):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, id_beneficio, ativo FROM beneficio_funcionario;
        """

        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "id_funcionario": r[1], "id_beneficio" : r[2], "ativo" : r[3] }
            for r in rows
        ]

    def update(self,  id_beneficio_funcionario, ativo = None ):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        fields = []
        values = []
        
        if ativo is not None:

            fields.append("ativo = %s")
            values.append(ativo)

        if not fields:
            
            cur.close()
            conn.close()
            return False

        query = f"""
                UPDATE beneficio_funcionario
                SET {','.join(fields) }
                WHERE id = %s;
        """

        values.append(id_beneficio_funcionario)
        cur.execute(query, values)

        cur.close()
        conn.close()
        return True


    def delete(self, id_beneficio_funcionario):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                DELETE FROM beneficio_funcionario
                WHERE id = %s;
        """

        cur.execute(query, (id_beneficio_funcionario,))

        cur.close()
        conn.close()
        return id_beneficio_funcionario

    #/////////////////////////
    #Métodos adicionais
    #/////////////////////////

    def get_by_funcionario(self, id_funcionario):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, id_beneficio, ativo FROM beneficio_funcionario
                WHERE id_funcionario = %s;
        """

        cur.execute(query, (id_funcionario,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "id_funcionario": r[1], "id_beneficio" : r[2], "ativo" : r[3] }
            for r in rows
        ]
    
    def get_by_beneficio(self, id_beneficio):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, id_beneficio, ativo FROM beneficio_funcionario
                WHERE id_beneficio = %s;
        """

        cur.execute(query, (id_beneficio,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "id_funcionario": r[1], "id_beneficio" : r[2], "ativo" : r[3] }
            for r in rows
        ]
    
    def delete_by_funcionario(self, id_funcionario):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                DELETE FROM beneficio_funcionario
                WHERE id_funcionario = %s;
        """


        cur.close()
        conn.close()
        return True
    
    def get_by_funcionario_e_beneficio(self, id_funcionario, id_beneficio):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, id_beneficio, ativo FROM beneficio_funcionario
                WHERE id_funcionario = %s AND id_beneficio = %s;
        """

        cur.execute(query, (id_funcionario, id_beneficio))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "id_funcionario" : row[1],
                "id_beneficio" : row[2],
                "ativo" : row[3]
            }

        return None