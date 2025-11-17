from config.connection import db_connection

class LogsAcessoRepository:
    
    def __init__(self, conn_factory = db_connection):
        self.conn_factory = conn_factory

    def create(self, id_usuario, operacao, consulta, result_count, time_stamp, ip):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                INSERT INTO logs_acesso (id_usuario, operacao, consulta, result_count, time_stamp, ip )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
        """

        cur.execute(query, ( id_usuario, operacao, consulta, result_count, time_stamp, ip))
        id_logs_acesso = cur.fetchone()[0]

        cur.close()
        conn.close()
        return id_logs_acesso
    
    def get_by_id(self, id_logs_acesso):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_usuario, operacao, consulta, result_count, time_stamp, ip FROM logs_acesso
                WHERE id = (%s);
        """

        cur.execute(query, (id_logs_acesso))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row:
            return{
                "id" : row[0],
                "id_usuario" : row[1],                
                "operacao" : row[2],
                "consulta" : row[3],
                "result_count" : row[4],
                "time_stamp" : row[5],
                "ip" : row[6]
            }

        return None

    def get_all(self):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_usuario, operacao, consulta, result_count, time_stamp, ip FROM logs_acesso;
        """

        cur.execute(query)
        rows = cur.fetchall

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "id_usuario" : r[1], "operacao" : r[2], "consulta" : r[3], "result_count": r[4], "time_stamp" : r[5], "ip" : r[6] }
            for r in rows
        ]
    
    def get_by_usuario(self, id_usuario):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_usuario, operacao, consulta, result_count, time_stamp, ip FROM logs_acesso
                WHERE id_usuario = (%s);
        """

        cur.execute(query, (id_usuario))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "id_usuario" : r[1], "operacao" : r[2], "consulta" : r[3], "result_count": r[4], "time_stamp" : r[5], "ip" : r[6] }
            for r in rows
        ]
    
    def get_by_time_range(self, start_time, end_time):

        conn = self.conn_factory()
        
        cur = conn.cursor()

        query = """
                SELECT id, id_usuario, operacao, consulta, result_count, time_stamp, ip FROM logs_acesso
                WHERE time_stamp BETWEEN %s AND %s;
        """

        cur.execute(query, (start_time, end_time))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {"id" : r[0], "id_usuario" : r[1], "operacao" : r[2], "consulta" : r[3], "result_count": r[4], "time_stamp" : r[5], "ip" : r[6] }
            for r in rows
        ]

    #//////////////////////////////////////////////////////////////////////////////////////////////////
    #ESSE REPOSITÓRIO NÃO POSSUI UPDATE, POIS OS LOGS DEVEM SER PERMANENTES E NÃO PODEM SER MODIFICADOS
    #//////////////////////////////////////////////////////////////////////////////////////////////////

    #//////////////////////////////////////////////////////////////////////////////////////////////////
    #ESSE REPOSITÓRIO NÃO POSSUI UPDATE, POIS OS LOGS DEVEM SER PERMANENTES E NÃO PODEM SER MODIFICADOS
    #//////////////////////////////////////////////////////////////////////////////////////////////////
