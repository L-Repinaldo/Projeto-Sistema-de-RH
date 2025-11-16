
class FuncionariosRepository():
    
    def __init__(self, conn_factory):
        self.conn_factory = conn_factory

    def create(self, nome, sobrenome, cpf, email, id_setor, cargo, faixa_salarial, data_nascimento, data_admissao):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO funcionarios (nome, sobrenome, cpf, email, cargo, faixa_salarial, data_nascimento, data_admissao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
        """

        cur.execute(query, (nome, sobrenome, cpf, email, id_setor, cargo, faixa_salarial, data_nascimento, data_admissao))
        funcionario_id = cur.fetchone()[0]

        cur.close()
        conn.close()
        return funcionario_id
    
    
    def get_by_id(self, funcionario_id):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, sobrenome, cpf, email, id_setor, cargo, faixa_salarial, data_nascimento, data_admissao FROM funcionarios
                WHERE id = (%s);
        """

        cur.execute(query, (funcionario_id))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "nome" : row[1],
                "sobrenome" : row[2],
                "cpf" : row[3],
                "email" : row[4],
                "id_setor" : row[5],
                "cargo" : row[6],
                "faixa_salarial" : row[7],
                "data_nascimento" : row[8],
                "data_admissao" : row[9] 
            }

        return None

    def get_all(self):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, nome, sobrenome, cpf, email, id_setor, cargo, faixa_salarial, data_nascimento, data_admissao FROM funcionarios;
        """

        cur.execute(query)
        rows = cur.fetchall

        cur.close()
        conn.close()

        return [
            {
                "id" : r[0],
                "nome" : r[1],
                "sobrenome" : r[2],
                "cpf" : r[3],
                "email" : r[4],
                "id_setor" : r[5],
                "cargo" : r[6],
                "faixa_salarial" : r[7],
                "data_nascimento" : r[8],
                "data_admissao" : r[9] 
            }
            for r in rows
        ]

    def update(self,  funcionario_id, nome = None, sobrenome = None, email = None, id_setor = None, cargo = None, faixa_salarial = None):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        fields = []
        values = []

        if nome is not None:

            fields.append("nome = %s")
            values.append(nome)
        
        if sobrenome is not None:

            fields.append("sobrenome = %s")
            values.append(sobrenome)

        if email is not None:

            fields.append("email = %s")
            values.append(email)

        if id_setor is not None:

            fields.append("id_setor = %s")
            values.append(id_setor)

        if cargo is not None:

            fields.append("cargo = %s")
            values.append(cargo)

        if faixa_salarial is not None:

            fields.append("faixa_salarial = %s")
            values.append(faixa_salarial)

        if not fields:
            
            cur.close()
            conn.close()
            return False

        query = f"""
                UPDATE funcionarios
                SET {','.join(fields) }
                WHERE id = %s;
        """

        values.append(funcionario_id)
        cur.execute(query, values)

        cur.close()
        conn.close()
        return True


    def delete(self, funcionario_id):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                DELETE FROM funcionarios
                WHERE id = %s;
        """

        cur.execute(query, (funcionario_id))

        cur.close()
        conn.close()
        return funcionario_id
