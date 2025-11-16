from config.connection import db_connection

class SetoresRepository():
    
    def __init__(self, conn_factory = db_connection):
        self.conn_factory = conn_factory

    #/////////////////////////
    #CRUD Basico
    #/////////////////////////


    def create(self, nome, id_gerente = None):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO setores (nome, id_gerente)
                VALUES (%s, %s)
                RETURNING id;
        """

        cur.execute(query, (nome, id_gerente))
        setor_id = cur.fetchone()[0]

        cur.close()
        conn.close()
        return setor_id
    
    def get_by_id(self, id_setor):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, id_gerente FROM setores
                WHERE id = (%s);
        """

        cur.execute(query, (id_setor))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "nome" : row[1],
                "id_gerente" : row[2]
            }

        return None

    def get_all(self):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, id_gerente FROM setores;
        """

        cur.execute(query)
        rows = cur.fetchall

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "nome": r[1], "id_gerente" : r[2]}
            for r in rows
        ]

    def update(self,  id_setor, nome = None, id_gerente = None):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        fields = []
        values = []

        if nome is not None:

            fields.append("nome = %s")
            values.append(nome)
        
        if id_gerente is not None:

            fields.append("id_gerente = %s")
            values.append(id_gerente)

        if not fields:
            
            cur.close()
            conn.close()
            return False

        query = f"""
                UPDATE setores
                SET {','.join(fields) }
                WHERE id = %s;
        """

        values.append(id_setor)
        cur.execute(query, values)

        cur.close()
        conn.close()
        return True


    def delete(self, id_setor):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                DELETE FROM setores
                WHERE id = %s;
        """

        cur.execute(query, (id_setor))

        cur.close()
        conn.close()
        return id_setor
    

    #/////////////////////////
    #Métodos adicionais
    #/////////////////////////

    def get_by_name(self, nome):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, id_gerente FROM setores
                WHERE nome = (%s);
        """

        cur.execute(query, (nome))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "nome" : row[1],
                "id_gerente" : row[2]
            }

        return None
    
    def get_by_gerente(self, id_gerente):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, id_gerente FROM setores
                WHERE id_gerente = (%s);
        """

        cur.execute(query, (id_gerente))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "nome" : row[1],
                "id_gerente" : row[2]
            }

        return None