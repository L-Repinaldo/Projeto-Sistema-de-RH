from config.connection import db_connection

class BeneficiosRepository:
    
    def __init__(self, conn_factory = db_connection):
        self.conn_factory = conn_factory

    def create(self, nome):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO beneficios (nome)
                VALUES (%s)
                RETURNING id;
        """

        cur.execute(query, (nome))
        setor_id = cur.fetchone()[0]

        cur.close()
        conn.close()
        return setor_id
    
    def get_by_id(self, id_beneficios):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome FROM beneficios
                WHERE id = (%s);
        """

        cur.execute(query, (id_beneficios))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "nome" : row[1]
            }

        return None

    def get_all(self):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome FROM beneficios;
        """

        cur.execute(query)
        rows = cur.fetchall

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "nome": r[1] }
            for r in rows
        ]

    def update(self,  id_beneficios, nome = None):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        fields = []
        values = []
        
        if nome is not None:

            fields.append("nome = %s")
            values.append(nome)

        if not fields:
            
            cur.close()
            conn.close()
            return False

        query = f"""
                UPDATE beneficios
                SET {','.join(fields) }
                WHERE id = %s;
        """

        values.append(id_beneficios)
        cur.execute(query, values)

        cur.close()
        conn.close()
        return True


    def delete(self, id_beneficios):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                DELETE FROM beneficios
                WHERE id = %s;
        """

        cur.execute(query, (id_beneficios))

        cur.close()
        conn.close()
        return id_beneficios
