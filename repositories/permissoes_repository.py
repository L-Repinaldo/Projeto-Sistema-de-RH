from config.connection import db_connection

class PermissoesRepository:
    def __init__(self, conn_factory = db_connection):
        self.conn_factory = conn_factory

    #/////////////////////////
    #CRUD Basico
    #/////////////////////////


    def create(self, nome):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO permissoes (nome)
                VALUES (%s)
                RETURNING id;
        """

        cur.execute(query, (nome,))
        id_permissao = cur.fetchone()[0]

        cur.close()
        conn.close()
        return id_permissao
    


    def get_by_id(self, id_permissao):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, ativo FROM permissoes
                WHERE id = (%s);
        """

        cur.execute(query, (id_permissao,))
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
                SELECT id, nome, ativo FROM permissoes;
        """

        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        permissoes = []
        for row in rows:
            permissoes.append({
                "id" : row[0],
                "nome" : row[1],
                "ativo" : row[2]
            })

        return permissoes

    def update(self, id_permissao, nome):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                UPDATE permissoes
                SET 
                    nome = COALESCE(%s, nome)
                    
                WHERE id = %s;
        """

        cur.execute(query, (nome, id_permissao))
        conn.commit()

        cur.close()
        conn.close()
        return True
    

    #/////////////////////////
    #Métodos adicionais
    #/////////////////////////


    def desactivate(self, id_permissao):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                UPDATE permissoes
                SET ativo = FALSE
                WHERE id = %s;
        """

        cur.execute(query, (id_permissao,))
        conn.commit()

        cur.close()
        conn.close()
        return True
    
    def activate(self, id_permissao):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                UPDATE permissoes
                SET ativo = TRUE
                WHERE id = %s;
        """

        cur.execute(query, (id_permissao,))
        conn.commit()

        cur.close()
        conn.close()
        return True
    
    def get_by_nome(self, nome):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, ativo FROM permissoes
                WHERE nome = (%s);
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