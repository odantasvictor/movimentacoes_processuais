import os
from datetime import datetime
from consultas_classesmetod import *
from consultas_funcoes import *
from bots_pje import BotsPje

# CONFIGURAÇÃO DE DATA
date_func = datetime.now()
date_today = date_func.strftime('%d-%m-%Y')

# CONFIGURAÇÃO DE DIRETÓRIOS E ARQUIVOS
directory_path = f'C:\\consulta_pjepb'
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
planilha_consulta = f'{directory_path}\\{date_func.strftime("%d-%m-%Y")}.xlsx'
planilha_resultado = f'{directory_path}\\resultados_{date_func.strftime("%d-%m-%Y")}.xlsx'

# CONFIGURAÇÃO DO SELENIUM WEBDRIVER
config = ConfigDriver
web_driver = config.driver_config(downloaddir=directory_path, user_data_dir=f'C:\\seleniumPJE')
pje = BotsPje(web_driver)

# CONFIGURAÇÃO DAS PLANILHAS XLSX PANDAS
pd = ConfigPdXlsx(consulta=planilha_consulta, resultado=planilha_resultado)
df_resultado = pd.ler_xlsx_resultado()
df_consulta = pd.ler_xlsx_consulta()

# VERIFICAR PROCESSOS CONSULTADOS E À CONSULTAR
lista_consultados = pd.ler_processos_consultados()
lista_a_consultar = pd.listar_processos_consulta()
print(f'{len(lista_a_consultar)} processos totais. {len(lista_a_consultar)-len(lista_consultados)} processos para consultar. {len(lista_consultados)} já consultados.')

# INICIAR ANÁLISE DOS PROCESSOS
for index, processo in enumerate(lista_a_consultar):
    numero_processo = formata_numproc(processo)
    pje.iniciar_consulta_publica(numero_processo[16:20])
    resultado_busca = pje.consultar_processo(numero_processo)
    if resultado_busca == 1:
        pje.abrir_processo()
        pje.coletar_movimentacoes(pandas=pd, processo=processo)
        pje.fechar_processo()