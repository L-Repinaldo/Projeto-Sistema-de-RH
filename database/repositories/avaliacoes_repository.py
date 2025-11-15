
class AvaliacoesRepository():
    
    def __init__(self, conn_factory):
        self.conn_factory = conn_factory

    def create(self, id_funcionario, data_avaliacao, nota):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO avalacoes (id_funcionario, data_avaliacao, nota)
                VALUES (%s, %s, %s)
                RETURNING id;
        """

        cur.execute(query, (id_funcionario, data_avaliacao, nota))
        setor_id = cur.fetchone()[0]

        cur.close()
        conn.close()
        return setor_id
    
    def get_by_id(self, id_avaliacoes):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, data_avaliacao, nota FROM avaliacoes
                WHERE id = (%s);
        """

        cur.execute(query, (id_avaliacoes))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "id_funcionario" : row[1],
                "data_avaliacao" : row[2],
                "nota" : row[3]
            }

        return None

    def get_all(self):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_funcionario, data_avaliacao, nota FROM avaliacoes;
        """

        cur.execute(query)
        rows = cur.fetchall

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "id_funcionario": r[1], "data_avaliacao" : r[2], "nota" : r[3]}
            for r in rows
        ]

    def update(self,  id_avaliacoes, id_funcionario = None, nota = None):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        fields = []
        values = []

        if id_funcionario is not None:

            fields.append("id_funcionario = %s")
            values.append(id_funcionario)
        
        if nota is not None:

            fields.append("nota = %s")
            values.append(nota)

        if not fields:
            
            cur.close()
            conn.close()
            return False

        query = f"""
                UPDATE avaliacoes
                SET {','.join(fields) }
                WHERE id = %s;
        """

        values.append(id_avaliacoes)
        cur.execute(query, values)

        cur.close()
        conn.close()
        return True


    def delete(self, id_avaliacoes):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                DELETE FROM avaliacoes
                WHERE id = %s;
        """

        cur.execute(query, (id_avaliacoes))

        cur.close()
        conn.close()
        return id_avaliacoes
