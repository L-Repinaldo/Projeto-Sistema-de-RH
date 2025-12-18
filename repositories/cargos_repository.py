from config.connection import db_connection

class CargosRepository:
    
    def __init__(self, conn_factory = db_connection):
        self.conn_factory = conn_factory

    def create(self, nome):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO cargos (nome)
                VALUES (%s)
                RETURNING id;
        """

        cur.execute(query, (nome,))
        id_cargo = cur.fetchone()[0]

        cur.close()
        conn.close()
        return id_cargo
    
    def get_by_id(self, id_cargo):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, ativo FROM cargos
                WHERE id = (%s);
        """

        cur.execute(query, (id_cargo,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "nome" : row[1],
                "ativo" : row[2]
            }

        return None

    def get_by_name(self, nome):

        conn = self.conn_factory()

        cur = conn.cursor()

        query = """
                SELECT id, nome, ativo FROM cargos
                WHERE nome ILIKE (%s);
        """

        cur.execute(query, (nome,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "nome" : row[1],
                "ativo" : row[2]
            }

        return None
    
    def get_all(self):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, ativo FROM cargos;
        """

        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "nome": r[1], "ativo" : r[2] }
            for r in rows
        ]
    
    def update(self,  id_cargo, nome):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                UPDATE cargos
                SET 
                    nome = COALESCE(%s, nome)
                    
                WHERE id = %s;
        """

        cur.execute(query, (nome, id_cargo))
        conn.commit()

        cur.close()
        conn.close()
        return True
    
    def  desactivate(self, id_cargo):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                UPDATE cargos
                SET ativo = FALSE
                WHERE id = %s;
        """

        cur.execute(query, (id_cargo,))
        conn.commit()

        cur.close()
        conn.close()
        return True
    
    def activate(self, id_cargo):

        conn = self.conn_factory()

        cur = conn.cursor()

        query = """
                UPDATE cargos
                SET ativo = TRUE
                WHERE id = %s;
        """
        cur.execute(query, (id_cargo,))
        conn.commit()

        cur.close()
        conn.close()
        return True