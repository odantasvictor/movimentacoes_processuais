import os
from typing import List
import pandas as pd
from datetime import datetime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PandasXlsx(metaclass=Singleton):

    def __init__(self, caminho_padrao: str) -> None:

        if not os.path.exists(caminho_padrao):
            os.makedirs(caminho_padrao)
        self.tabela_consulta = f'{caminho_padrao}/{datetime.now().strftime("%d-%m-%Y")}.xlsx'
        self.tabela_resultado = f'{caminho_padrao}/{datetime.now().strftime("%d-%m-%Y")}_resultado.xlsx'
        self.df_consulta = self.ler_xlsx_consulta()
        self.df_resultado = self.ler_xlsx_resultado()
        self.lista_consultados = []
        self.lista_consultar = []

    def ler_xlsx_consulta(self):
        try:
            self.df_consulta = pd.read_excel(self.tabela_consulta)
            return self.df_consulta
        except Exception as e:
            return e

    def listar_processos_consulta(self):
        try:
            for processo in self.df_consulta['Processos'].items():
                if processo not in self.lista_consultados:
                    self.lista_consultar.append(processo[1])
            return self.lista_consultar
        except Exception as e:
            return e

    def ler_xlsx_resultado(self):
        try:
            self.df_resultado = pd.read_excel(self.tabela_resultado)
            return self.df_resultado
        except Exception as e:
            self.df_resultado = pd.DataFrame({'Processo': [], 'UF': [], 'Movimentação': [], 'Data da Movimentação': [], 'Feedback': [], 'URL Consulta': []})
            self.df_resultado.to_excel(self.tabela_resultado, index=False)
            return self.df_resultado

    def ler_processos_consultados(self):
        try:
            for processo in self.df_resultado['Processo'].items():
                if processo not in self.lista_consultados:
                    self.lista_consultados.append(processo[1])
            return self.lista_consultados
        except Exception as e:
            return e

    def lancar_movimentacoes(self, processo: str, uf: str, lista_movimentacoes: List[List]):
        for movimentacao in lista_movimentacoes:
            movimentacao = [processo, uf] + movimentacao
            try:
                self.df_resultado.loc[len(self.df_resultado.index)] = movimentacao
                self.df_resultado.to_excel(self.tabela_resultado, index=False)
                print(f'Movimentacação {movimentacao} anotada com sucesso na planilha')
            except Exception as e:
                return e

