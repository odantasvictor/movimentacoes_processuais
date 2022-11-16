from typing import List
from mysql.connector import connect, Error
from base.config import Configuracoes
from base.util import *
from datetime import datetime
config = Configuracoes()
 

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):

    def __init__(self):
        self.connection = connect(
            host = config.getstring('Database', 'db_host'),
            user = config.getstring('Database', 'db_user'),
            password = config.getstring('Database', 'db_pass'),
            database = config.getstring('Database', 'db_name'),
            port = config.getinteger('Database', 'db_port'),
            use_unicode=True,
            charset='utf8'
        )
        try:
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                info = self.connection.get_server_info()
                print("Conectado ao MySQL Server versão:", info)
                cursor.execute("select database();")
                record = cursor.fetchall()
                print("Conectado ao banco de dados: ", record)

        except Error as e:
            print("Error durante a conexão ao MySQL:", e)

    def listar_processos_atualizar(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM `processos` WHERE ultima_atualizacao<='{datetime.now().strftime('%Y-%m-%d')}' OR ultima_atualizacao IS NULL")
        registros_banco = cursor.fetchall()
        lista_processos = [tupla_processo[1] for tupla_processo in registros_banco]
        return lista_processos
    
    def lancar_movimentacoes(self, processo: str, uf: str, lista_movimentacoes: List[List]):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM `processos` WHERE processo='{processo}'")
        id_processo = cursor.fetchall()[0][0]

        for movimentacao in lista_movimentacoes:
            data_formatada = formata_data_pje(movimentacao[1])
            cursor.execute(f"SELECT * FROM `movimentacoes` WHERE id_processo='{id_processo}' AND data_movimentacao='{data_formatada}'")
            prevencao_duplicidade = cursor.fetchall()
            if prevencao_duplicidade ==  []:
                self.execute_query(f"INSERT INTO movimentacoes(id_processo, movimentacao, data_movimentacao) VALUES ({id_processo}, '{movimentacao[0]}', '{data_formatada}')")
        self.execute_query(f"UPDATE processos SET ultima_atualizacao='{datetime.now().strftime('%Y-%m-%d')}', uf='{uf}' WHERE id_processo={id_processo}")


    def execute_query(self, query):
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(query)
        self.connection.commit()
        print(f'Query {query} executada com sucesso.')
